from flask_socketio import SocketIO, emit
from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
import logging
import os
import sys
from config import *
from processing.file_upload import upload_file
from routes.pdf_processing import perform_action
from routes.folder_operations import is_upload_folder_empty, empty_upload_folder
from utilsssss.cleanup import scheduler
from utilsssss.cors_config import get_allowed_origins
from db.database_module import fetch_invoice_data_from_db


app = Flask(__name__)
origins = get_allowed_origins()
CORS(app, resources={r"/api/*": {"origins": origins}})
socketio = SocketIO(app, cors_allowed_origins="*")

logging.basicConfig(level=LOG_LEVEL)


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    try:
        emit('connection_established', {'message': 'Welcome!'})

    except Exception as e:
        print(f"Error during connection handling: {e}")
        emit('error', {'message': 'An error occurred.'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    logging.info("Client disconnected")


@socketio.on_error_default
def default_error_handler(error):
    print(f"An error occurred: {error}")
    socketio.emit('error', {'message': 'An internal server error occurred.'})


@app.route('/api')
def index():
    print('Client connected')
    return 'Client connected!'


@app.route('/api/upload', methods=['POST'])
def handle_file_upload():
    return upload_file(socketio)


@app.route('/api/totals')
def process_pdf():
    return perform_action(socketio)


@app.route('/api/results/<batch_id>', methods=['GET'])
def get_invoice_data(batch_id):
    # Fetch invoice data from the database based on batch_id
    # You'll need to implement this function
    data = fetch_invoice_data_from_db(batch_id)
    return jsonify(data)


@app.route('/api/empty', methods=['POST'])
def empty_upload_folder_route():
    return empty_upload_folder()


@app.route('/api/check-folder', methods=['GET'])
def check_upload_folder():
    return is_upload_folder_empty()


mode = MODE

if __name__ == '__main__':
    port = 5001

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[sys.argv.index("--port") + 1])
        except (ValueError, IndexError):
            print("Invalid or missing port value. Using default port 5000.")

    port = int(os.getenv("PORT", port))

    scheduler.start()

    if mode == "local":
        socketio.run(app, host='0.0.0.0', port=port)
    else:
        serve(app, host='0.0.0.0', port=port, threads=4)
