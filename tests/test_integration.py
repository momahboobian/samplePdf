import os
import time
import pytest
from app import app, socketio
from flask_socketio import SocketIOTestClient

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

@pytest.fixture
def setup_and_teardown():
    # Ensure cleanup before and after tests
    yield
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def test_upload_and_process_files(client, socket_client, setup_and_teardown):
    # Upload a file
    data = {
        'files[]': (open('path/to/your/testfile.pdf', 'rb'), 'testfile.pdf')
    }
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert b'Files uploaded successfully' in response.data

    # Process the file
    response = client.get('/api/totals')
    assert response.status_code == 200
    assert b'site_totals' in response.data

    # Check WebSocket events
    with socket_client as client:
        @client.on('invoice_processed')
        def handle_invoice_processed(data):
            assert 'file' in data
            assert 'total' in data
        @client.on('processing_complete')
        def handle_processing_complete(data):
            assert 'grand_total' in data
