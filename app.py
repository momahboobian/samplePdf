from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from waitress import serve
import logging
import sys
import os
from config import *

from processing.file_upload import upload_file
from utils.cors_config import get_allowed_origins
from utils.cleanup import scheduler
from database.schema import create_tables, populate_sites_table
from utils.logger import setup_logger

app = Flask(__name__)
origins = get_allowed_origins()
CORS(app, resources={r"/api/*": {"origins": origins}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure logging
setup_logger()
logger = logging.getLogger(__name__)


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
    # print('Client disconnected')
    logging.info("Client disconnected")


@socketio.on_error_default
def default_error_handler(error):
    print(f"An error occurred: {error}")
    socketio.emit('error', {'message': 'An internal server error occurred.'})


# Call functions to create tables and populate sites on app startup
with app.app_context():
    create_tables()
    populate_sites_table()


@app.route('/api')
def index():
    logger.info('Client connected to /api')
    return 'Client connected!'


@app.route('/api/upload', methods=['POST'])
def handle_file_upload():
    return upload_file(socketio)


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
