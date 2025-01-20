import os
import time
import logging
import uuid
from flask import jsonify, request

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

        for file in files:
            if file and file.filename.endswith('.pdf'):
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{file.filename}"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                logging.info(f"File saved successfully at: {file_path}")
            else:
                return jsonify({'error': 'Invalid file format, must be a PDF'}), 400

        return jsonify({
            'message': 'Files uploaded successfully',
            'folder': folder_name,
            'batch_id': batch_id,
            'total_files': total_files
        }), 200

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500
