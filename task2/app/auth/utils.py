from werkzeug.utils import secure_filename
import os

def save_uploaded_image(image_data):
    UPLOAD_FOLDER = 'lab10/app/static/profile_pics'
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(image_data.filename)

    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image_data.save(image_path)

    return filename