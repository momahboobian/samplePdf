import pytest
from app import app, socketio
from flask import jsonify
from flask_socketio import SocketIOTestClient

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def socket_client():
    test_client = SocketIOTestClient(app)
    yield test_client

def test_handle_file_upload(client):
    data = {
        'files[]': (open('path/to/your/testfile.pdf', 'rb'), 'testfile.pdf')
    }
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert b'Files uploaded successfully' in response.data

def test_process_pdf(client):
    response = client.get('/api/totals')
    assert response.status_code == 200
    assert b'site_totals' in response.data
