import os
from dotenv import load_dotenv

load_dotenv('.env')

ALLOWED_ORIGINS = ["https://pdf-analysis.moreel.me", "http://localhost:3030"]

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
LOG_LEVEL = 'DEBUG'

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

MODE = os.environ.get('MODE')
