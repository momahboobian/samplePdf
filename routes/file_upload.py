import os
import time
import logging
import uuid
from flask import jsonify, request
from flask_socketio import emit


# Set up logging
logging.basicConfig(level=logging.DEBUG)

def upload_file():
    try:
        batch_id = str(uuid.uuid4())
        folder_name = request.form.get('folder')

        if not folder_name:
            return jsonify({'error': 'Folder name is required'}), 400

        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400

        files = request.files.getlist('files[]')
        total_files = len(files)

        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', folder_name, batch_id)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Emit an event to start the upload process
        emit('upload_started', {'batch_id': batch_id, 'total_files': total_files})

        # Iterate over each file
        for index, file in enumerate(files):
            if file and file.filename.endswith('.pdf'):
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{file.filename}"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                
                # Emitting progress for the current file upload
                file_size = len(file.read())  # Get the size of the file
                file.seek(0)  # Reset file pointer to start
                
                # Upload file in chunks and emit progress updates
                chunk_size = 1024  # Define chunk size (1 KB for example)
                uploaded = 0
                while chunk := file.read(chunk_size):
                    with open(file_path, 'ab') as f:
                        f.write(chunk)
                        uploaded += len(chunk)
                    progress = int((uploaded / file_size) * 100)
                    emit('file_upload_progress', {'filename': file.filename, 'progress': progress, 'batch_id': batch_id})
                
                logging.info(f"File saved successfully at: {file_path}")
            else:
                return jsonify({'error': 'Invalid file format, must be a PDF'}), 400

        # After upload, you can proceed to start the calculation process for totals
        emit('upload_complete', {'batch_id': batch_id, 'total_files': total_files})
        return jsonify({'message': 'Files uploaded successfully', 'batch_id': batch_id}), 200

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500