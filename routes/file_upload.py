from flask import jsonify, request
import os
import time
import logging

from utils.folder_utils import is_upload_folder_empty, empty_upload_folder

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    if not is_upload_folder_empty():
        return jsonify({'error': 'Upload folder is not empty. Do you want to empty it?'}), 409

    files = request.files.getlist('files[]')
    
    for file in files:
        if file and file.filename.endswith('.pdf'):
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            logging.info(f"File saved successfully at: {file_path}")
        else:
            return jsonify({'error': 'Invalid file format, must be a PDF'}), 400

    return jsonify({'message': 'Files uploaded successfully'}), 200