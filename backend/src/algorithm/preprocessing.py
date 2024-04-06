import os
import shutil
from PIL import Image

def produce_depth_map(picture_dir: str, picture_name: str):
    full_path = picture_dir + "/" + picture_name

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"The path {full_path} does not exists")
    if not os.path.isfile(full_path): 
        raise FileExistsError(f"The path {full_path} does not lead to a file")
    if _is_image_corrupted(full_path):
        raise FileExistsError(f"The file {full_path} exists but is corrupted or not an image")
    source_path = 'path/to/source/file.txt'
    destination_path = 'path/to/destination/'

    shutil.copyfile(source_path, destination_path + 'file.txt')



    


def _is_image_corrupted(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
            return False 
    except Exception as e:
        return True
        
produce_depth_map("dsa", "dsa")
