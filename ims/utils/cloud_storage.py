# ims/utils/cloud_storage.py
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = r"D:\sakna\Sakna Perera\Lec\Software Architecture and Programming\CW2\AIMS\abc_ims\uploads"

def save_file(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)
    return filename

def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
