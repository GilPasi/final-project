import os 
def infer_absolute_path(image_path, input_path):
    is_absolute_path = os.path.exists(image_path)
    if not is_absolute_path:
        image_path = os.path.join(input_path, image_path)
    if not os.path.exists(image_path): 
        raise ValueError(f"The given image path {image_path} is"
                            f" neither absolute nor a valid image\n "
                            f"name in the directory {input_path}.")
    return image_path

def get_mappify_root_dir():
    variable_name = 'MAPPIFY'
    mappify_path = os.getenv(variable_name, None)
    if mappify_path is None:
        raise ImportError("Mappify is not configured"
                         " properly to your environment variables,"
                         " re-configure and restart your IDE")
    return mappify_path