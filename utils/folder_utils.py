import os
import shutil

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def is_upload_folder_empty():
    if not os.path.exists(UPLOAD_FOLDER):
        return True
    return len(os.listdir(UPLOAD_FOLDER)) == 0



def empty_upload_folder():
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)

        for root, dirs, files in os.walk(UPLOAD_FOLDER, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(UPLOAD_FOLDER)
    os.makedirs(UPLOAD_FOLDER)
    return {"message": "Folder cleared successfully."}