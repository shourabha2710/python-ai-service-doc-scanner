import os

def save_temp_file(upload_file, folder="temp"):

    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, upload_file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())

    return file_path