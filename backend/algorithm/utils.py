import os 
SNAPSHOT_SIZE = (256, 256)

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

def get_default_input_path():
    return os.path.join(
        get_mappify_root_dir(), "backend","algorithm","input") 

def get_algorithm_dir():
    return os.path.join(get_mappify_root_dir(), "backend", "algorithm")

def ipc_file_path(env_name):
    file_name = f"{env_name}_ipc.pkl"
    path = os.path.join(get_mappify_root_dir(), "backend", "algorithm", file_name)
    return path

def list_directory_contents(directory_path, allowed_extentsions=[]):
    """Lists the names and paths of all files and directories in the specified directory."""
    
    entries = os.listdir(directory_path)
    all_contents = []
    allow_all = allowed_extentsions == [] 

    for entry in entries:
        root, ext = os.path.splitext(entry) # Get extention
        if allow_all or ext in allowed_extentsions:
            full_path = os.path.join(directory_path, entry)
            all_contents.append(full_path)
    return all_contents

