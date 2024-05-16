from flask import jsonify
import os
import shutil

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def is_folder_empty():
    return not os.path.isdir(UPLOAD_FOLDER)

def empty_folder():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    return jsonify({'message': 'Upload folder emptied successfully.'}), 200