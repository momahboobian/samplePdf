from flask_socketio import SocketIO, emit
from flask import Flask, request
from flask_cors import CORS
import logging
import os
import sys

from config import LOG_LEVEL
from routes.file_upload import upload_file
from routes.pdf_processing import perform_action
from routes.folder_operations import is_upload_folder_empty, empty_upload_folder
from utils.cleanup import scheduler
# from db.populate_data import populate_data

app = Flask(__name__)
# CORS(app, origin=["https://pdf-analysis.moreel.me", "https://pdf-analysis.moreel.me/api"])
CORS(app, resources={r"/api/*": {"origins": "*"}})
origins = ["https://pdf-analysis.moreel.me", "https://pdf-analysis.moreel.me/api","https://pdf-analysis.moreel.me/socket.io", "http://localhost:3030"]
socketio = SocketIO(app, cors_allowed_origins="*")

# Set up logging
logging.basicConfig(level=LOG_LEVEL)

# Socket Event: Start population
@socketio.on('connect')

@app.route('/api/')
def index():
    print('Client connected')
    return 'Client connected!'


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
    port = 5001

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[sys.argv.index("--port") + 1])
        except (ValueError, IndexError):
            print("Invalid or missing port value. Using default port 5000.")
    
    port = int(os.getenv("PORT", port))

    scheduler.start()
    socketio.run(app, host='0.0.0.0', port=port)
