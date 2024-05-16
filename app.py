from flask import Flask
from flask_cors import CORS
import logging

from routes.file_upload import upload_file
from routes.pdf_processing import perform_action
from routes.folder_operations import is_folder_empty, empty_folder
from config import LOG_LEVEL

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=LOG_LEVEL)

@app.route('/')
def index():
    return 'Backend is working!'

@app.route('/upload', methods=['POST'])
def handle_file_upload():
    return upload_file()

@app.route('/totals')
def process_pdf():
    return perform_action()

@app.route('/empty', methods=['POST'])
def empty_upload_folder():
    return empty_folder()

@app.route('/check-folder', methods=['GET'])
def check_upload_folder():
    return is_folder_empty()

if __name__ == '__main__':
    app.run(host='0.0.0.0')