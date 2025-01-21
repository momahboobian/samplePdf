import os
import logging
import uuid
from flask import jsonify, request
from flask_socketio import emit
from utils.calcSiteTotals import calculate_site_totals


# Set up logging
logging.basicConfig(level=logging.DEBUG)

def upload_file():
    try:
        folder_name = request.form.get('folder')
        if not folder_name:
            return jsonify({'error': 'Folder name is required'}), 400

        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400

        files = request.files.getlist('files[]')
        total_files = len(files)

        batch_id = str(uuid.uuid4())
        upload_folder = os.path.join(os.getcwd(), 'uploads', folder_name)
        os.makedirs(upload_folder, exist_ok=True)


        for file in files:
            if file and file.filename.endswith('.pdf'):
                filename = file.filename
                file_path = os.path.join(upload_folder, filename)

                save_file_with_progress(file, file_path, batch_id, filename)

                logging.info(f"File saved successfully at: {file_path}")

                # Call the calculate_site_totals function
                calculate_site_totals(upload_folder)
                logging.info("Site totals calculated successfully")
            else:
                emit('file_upload_error', {
                    'batch_id': batch_id,
                    'error_message': 'Invalid file format, must be a PDF'
                })
                return jsonify({'error': 'Invalid file format, must be a PDF'}), 400

        # Send live feedback to the client
        emit('file_upload_complete', {
            'batch_id': batch_id,
            'total_files': total_files
        }, namespace='/', broadcast=True)


        return jsonify({
            'message': 'Files uploaded successfully',
            'folder': folder_name,
            'total_files': total_files,
            'batch_id': batch_id,
            'upload_folder': upload_folder
        }), 200

    except Exception as e:
        emit('file_upload_error', {
            'batch_id': str(uuid.uuid4()),
            'error_message': str(e)
        }, namespace='/', broadcast=True)
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500
    
def save_file_with_progress(file, file_path, batch_id, filename):
    chunk_size = 1524000  # 1.5MB
    total_size = file.content_length if file.content_length else 0
    uploaded_size = 0

    with open(file_path, 'wb') as f:
        while chunk := file.stream.read(chunk_size):
            f.write(chunk)
            uploaded_size += len(chunk)
            progress = (uploaded_size / total_size) * 100 if total_size else 100
            emit('file_upload_progress', {
                'batch_id': batch_id,
                'file_name': filename,
                'file_size': total_size,
                'progress': progress
            }, namespace='/', broadcast=True)