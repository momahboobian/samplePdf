from flask import jsonify, request
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def upload_file():
    try:
        # Get the folder name from the request
        folder_name = request.form.get('folder')
        if not folder_name:
            return jsonify({'error': 'Folder name is required'}), 400

        # Ensure files are present in the request
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400

        files = request.files.getlist('files[]')
        total_files = len(files)

        # Define the upload folder path
        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', folder_name)

        # Create the upload folder if it doesn't exist
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Iterate over the files and save them
        for file in files:
            if file and file.filename.endswith('.pdf'):
                # Generate a unique timestamp for the filename
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{file.filename}"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                logging.info(f"File saved successfully at: {file_path}")
            else:
                return jsonify({'error': 'Invalid file format, must be a PDF'}), 400

        # Return the folder name and the total number of uploaded files for further processing
        return jsonify({
            'message': 'Files uploaded successfully',
            'folder': folder_name,
            'total_files': total_files
        }), 200

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500
