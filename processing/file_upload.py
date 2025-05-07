import os
import logging
import uuid
from flask import jsonify, request
from utils.logger import setup_logger
from processing.processing_workflow import process_all_pdfs

# Set up logging
setup_logger()
logger = logging.getLogger(__name__)


def upload_file(socketio):
    logger.info("Received file upload request")

    try:
        folder_name = request.form.get('folder')
        if not folder_name:
            error_message = "Folder name is required"
            logger.warning(error_message)
            socketio.emit('file_upload_error', {'batch_id': str(
                uuid.uuid4()), 'error_message': error_message})
            return jsonify({'error': error_message}), 400

        if 'files[]' not in request.files:
            error_message = "No files uploaded"
            logger.warning(error_message)
            socketio.emit('file_upload_error', {'batch_id': str(
                uuid.uuid4()), 'error_message': error_message})
            return jsonify({'error': error_message}), 400

        files = request.files.getlist('files[]')
        total_files = len(files)
        logger.debug(f"Number of files uploaded: {total_files}")

        batch_id = str(uuid.uuid4())
        upload_folder = os.path.join(os.getcwd(), 'uploads', folder_name)
        os.makedirs(upload_folder, exist_ok=True)
        logger.debug(f"Upload folder created: {upload_folder}")

        for i, file in enumerate(files):
            logger.info(
                f"Processing file {i+1}/{total_files}: {file.filename}")

            if file and file.filename.endswith('.pdf'):
                filename = file.filename
                file_path = os.path.join(upload_folder, filename)

                try:
                    file.save(file_path)
                    logger.info(f"File saved: {filename} to {file_path}")
                except Exception as save_error:
                    error_message = f"Error saving file {filename}: {save_error}"
                    logger.error(error_message, exc_info=True)
                    socketio.emit('file_upload_error', {
                                  'batch_id': batch_id, 'error_message': error_message})
                    return jsonify({'error': error_message}), 500
            else:
                error_message = f"Invalid file format for {file.filename}"
                logger.warning(error_message)
                socketio.emit('file_upload_error', {
                              'batch_id': batch_id, 'error_message': error_message})
                return jsonify({'error': error_message}), 400

        success_message = "Files uploaded successfully"
        logger.info(f"Batch {batch_id}: {success_message}")
        socketio.emit('all_invoices_processed', {'batch_id': batch_id})

        #  Trigger PDF processing after successful upload
        process_all_pdfs(upload_folder, socketio)

        return jsonify({'batch_id': batch_id, 'message': success_message}), 200

    except Exception as e:
        error_message = f"Error processing upload: {e}"
        logger.error(error_message, exc_info=True)
        socketio.emit('file_upload_error', {'batch_id': str(
            uuid.uuid4()), 'error_message': error_message})
        return jsonify({'error': 'An internal server error occurred'}), 50000
