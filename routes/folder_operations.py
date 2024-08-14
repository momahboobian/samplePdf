from flask import jsonify
import os
import shutil
import logging

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def is_upload_folder_empty():
    # Check if the folder exists first
    if not os.path.exists(UPLOAD_FOLDER):
        logging.debug("Upload folder does not exist.")
        return {'folder_empty': True}
    
    # Check if the folder is empty
    is_empty = len(os.listdir(UPLOAD_FOLDER)) == 0
    return jsonify({'folder_empty': is_empty})


def empty_upload_folder():
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    return jsonify({'message': 'Upload folder emptied successfully.'}), 200
