from PIL import Image
from utils import list_directory_contents, prefix_from_absolute_path
import os 

def crop_image_to_square(image_path: str, output_path:str):
    image = Image.open(image_path)
    width, height = image.size
    min_dimension = min(width, height)

    left = (width - min_dimension) // 2
    top = (height - min_dimension) // 2
    right = left + min_dimension
    bottom = top + min_dimension
    cropped_image = image.crop((left, top, right, bottom))

    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    if not any(output_path.lower().endswith(ext) for ext in valid_extensions):
        raise ValueError(f"Invalid file extension in output path: {output_path}")

    
    cropped_image.save(output_path)

if __name__ == "__main__":
    
    input_path = "backend/algorithm/input/"
    all_images = list_directory_contents(input_path, [".jpg"])

    for path in all_images: 
        prefixed_path = prefix_from_absolute_path(path, "sqr_")
        crop_image_to_square(path,prefixed_path)