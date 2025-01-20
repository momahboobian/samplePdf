import os
from dotenv import load_dotenv

load_dotenv('.env')


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
LOG_LEVEL = 'DEBUG'

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')