import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

UPLOADS_DIR = os.path.join(os.getcwd(), 'uploads')
MAX_AGE_DAYS = 14  # 2 weeks

def cleanup_old_folders():
    now = time.time()
    cutoff = now - (MAX_AGE_DAYS * 86400)  # Convert days to seconds

    for folder in os.listdir(UPLOADS_DIR):
        folder_path = os.path.join(UPLOADS_DIR, folder)
        if os.path.isdir(folder_path):
            folder_mtime = os.path.getmtime(folder_path)
            if folder_mtime < cutoff:
                try:
                    os.rmdir(folder_path)  # Ensure the folder is empty before removal
                    print(f"Deleted old folder: {folder_path}")
                except OSError as e:
                    print(f"Error deleting folder {folder_path}: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_folders, 'interval', days=7)