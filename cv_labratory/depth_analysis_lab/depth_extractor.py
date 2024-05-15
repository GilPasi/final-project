import torch 
import sys
import os
from PIL import Image
# WARNING: do not change the location of this function in 
# order to avoid bugs.
def get_mappify_root_dir():
    variable_name = 'MAPPIFY'
    mappify_path = os.getenv(variable_name, None)
    if mappify_path is None:
        raise ImportError("Mappify is not configured"
                         " properly to your environment variables,"
                         " re-configure and restart your IDE")
    return mappify_path

zoe_directory = os.path.join(get_mappify_root_dir(),"backend/lib/ZoeDepth")
sys.path.append(zoe_directory)
from zoedepth.models.builder import build_model
from zoedepth.utils.config import get_config
from zoedepth.utils.misc import pil_to_batched_tensor
from zoedepth.utils.misc import save_raw_16bit
from zoedepth.utils.misc import colorize
 


# ZoeD_N
def produce_zoe(device):
    conf = get_config("zoedepth", "infer")
    model_zoe_n = build_model(conf)
    zoe = model_zoe_n.to(device)
    return zoe    

def load_images(image_relative_path="/input/"):
    mappify_path = get_mappify_root_dir()
    absolute_image_path = os.path.join(mappify_path
                    ,image_relative_path)  # load
    return [load_image(x) for x in list_files(absolute_image_path)]

def list_files(directory):
    files = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            files.append(filename)
        else: 
            raise TypeError(f"The directory {path} was found in the input directory"
                            "remove it to prevent missing data and run again")
    return files

def load_image(image_name, image_relative_path="cv_labratory/depth_analysis_lab/input"):
    mappify_path = get_mappify_root_dir()
    absolute_image_path = os.path.join(mappify_path, image_relative_path, image_name)
    image = Image.open(absolute_image_path).convert("RGB")
    return image

def save_product(depth, image_name, output_relative_path="cv_labratory/depth_analysis_lab/output/"):
    colored_image_name = "colored_" + image_name
    mappify_path = get_mappify_root_dir()
    absolute_output_path = os.path.join(
        mappify_path, output_relative_path, image_name)
    absolute_colored_output_path = os.path.join(
        mappify_path, output_relative_path, colored_image_name)
    # Save raw
    save_raw_16bit(depth, absolute_output_path)
    colored = colorize(depth)
    # save colored output
    Image.fromarray(colored).save(absolute_colored_output_path)
    
if __name__ == "__main__":
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    zoe = produce_zoe(DEVICE)
    image = load_image("1.png") 

    depth_numpy = zoe.infer_pil(image)  # as numpy
    depth_pil = zoe.infer_pil(image, output_type="pil")  # as 16-bit PIL Image
    depth_tensor = zoe.infer_pil(image, output_type="tensor")  # as torch tensor
    X = pil_to_batched_tensor(image).to(DEVICE)
    depth_tensor = zoe.infer(X)
    depth = zoe.infer_pil(image)

    print(depth_tensor)

    # fetch
    save_product(depth, "1.png")
