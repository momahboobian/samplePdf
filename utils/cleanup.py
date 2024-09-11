import os
import time
import shutil
from apscheduler.schedulers.background import BackgroundScheduler

UPLOADS_DIR = os.path.join(os.getcwd(), 'uploads')
MAX_AGE_DAYS = 7  # 1 week

def cleanup_old_folders():
    now = time.time()
    cutoff = now - (MAX_AGE_DAYS * 86400)  # Convert days to seconds

    for folder in os.listdir(UPLOADS_DIR):
        folder_path = os.path.join(UPLOADS_DIR, folder)
        if os.path.isdir(folder_path):
            folder_mtime = os.path.getmtime(folder_path)
            if folder_mtime < cutoff:
                try:
                    # Use shutil.rmtree to delete non-empty folders
                    shutil.rmtree(folder_path)
                    print(f"Deleted old folder: {folder_path}")
                except OSError as e:
                    print(f"Error deleting folder {folder_path}: {e}")

# Schedule the cleanup job to run every 7 days
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_folders, 'interval', days=7)
