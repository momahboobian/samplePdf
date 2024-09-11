from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import logging

from config import LOG_LEVEL
from routes.file_upload import upload_file
from routes.pdf_processing import perform_action
from routes.folder_operations import is_upload_folder_empty, empty_upload_folder
from utils.cleanup import scheduler 

app = Flask(__name__)
CORS(app, origin=["https://pdf-analysis.moreel.me/"])
socketio = SocketIO(app, cors_allowed_origins=["https://pdf-analysis.moreel.me/api", "http://localhost:3030"])

# Set up logging
logging.basicConfig(level=LOG_LEVEL)


@app.route('/api/')
def index():
    return 'Backend is working!'


@app.route('/api/upload', methods=['POST'])
def handle_file_upload():
    return upload_file()


@app.route('/api/totals')
def process_pdf():
    return perform_action(socketio)


@app.route('/api/empty', methods=['POST'])
def empty_upload_folder_route():
    return empty_upload_folder()


@app.route('/api/check-folder', methods=['GET'])
def check_upload_folder():
    return is_upload_folder_empty()


if __name__ == '__main__':
    scheduler.start()
    socketio.run(app, host='0.0.0.0')
