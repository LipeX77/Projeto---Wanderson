import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_DOCUMENT_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "webp"}
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_DOCUMENT_EXTENSIONS

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def save_uploaded_file(file_storage, subfolder="documents"):
    if not file_storage or not file_storage.filename:
        return None
        
    original_name = secure_filename(file_storage.filename)
    if not original_name:
        original_name = "file"
        
    ext = ""
    if "." in original_name:
        ext = "." + original_name.rsplit(".", 1)[1].lower()
        
    stored_name = f"{uuid.uuid4().hex}{ext}"
    
    upload_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder)
    os.makedirs(upload_folder, exist_ok=True)
    
    storage_path = os.path.join(upload_folder, stored_name)
    file_storage.save(storage_path)
    
    file_size = os.path.getsize(storage_path)
    mime_type = file_storage.content_type
    
    return {
        "original_name": file_storage.filename,
        "stored_name": stored_name,
        "storage_path": storage_path,
        "mime_type": mime_type,
        "file_size": file_size
    }
