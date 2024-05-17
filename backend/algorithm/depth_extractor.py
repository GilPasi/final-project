import torch 
import sys
import os
from PIL import Image
# WARNING: do not change the location of this function in 
# order to avoid bugs.
def _get_mappify_root_dir():
    variable_name = 'MAPPIFY'
    mappify_path = os.getenv(variable_name, None)
    if mappify_path is None:
        raise ImportError("Mappify is not configured"
                         " properly to your environment variables,"
                         " re-configure and restart your IDE")
    return mappify_path

zoe_directory = os.path.join(_get_mappify_root_dir(),"backend/lib/ZoeDepth")
sys.path.append(zoe_directory)
from zoedepth.models.builder import build_model
from zoedepth.utils.config import get_config
from zoedepth.utils.misc import pil_to_batched_tensor
from zoedepth.utils.misc import save_raw_16bit
from zoedepth.utils.misc import colorize
 
class DepthExtractor(): 
    def __init__(self, device):
        self._conf = get_config("zoedepth", "infer")
        model_zoe_n = build_model(self._conf)
        self._zoe = model_zoe_n.to(device)

    def list_files(self, directory):
        files = []
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            if os.path.isfile(path):
                files.append(filename)
            else: 
                raise TypeError(f"The directory {path} was found in the input directory"
                                "remove it to prevent missing data and run again")
        return files

    def load_image(self, image_name, image_relative_path="cv_labratory/depth_analysis_lab/input"):

        mappify_path = _get_mappify_root_dir()
        absolute_image_path = os.path.join(mappify_path, image_relative_path, image_name)
        image = Image.open(absolute_image_path).convert("RGB")
        return image

    def _save_product(self, depth, image_name, output_relative_path="cv_labratory/depth_analysis_lab/output/"):
        # This method is not actually required on production since there is no need to see the products.
        colored_image_name = "colored_" + image_name
        mappify_path = _get_mappify_root_dir()
        absolute_output_path = os.path.join(
            mappify_path, output_relative_path, image_name)
        absolute_colored_output_path = os.path.join(
            mappify_path, output_relative_path, colored_image_name)
        # Save raw
        save_raw_16bit(depth, absolute_output_path)
        colored = colorize(depth)
        # save colored output
        Image.fromarray(colored).save(absolute_colored_output_path)


# Demo for debugging
if __name__ == "__main__":
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    depth_extractor = DepthExtractor(DEVICE)
    image = depth_extractor.load_image("1.png") 

    depth_numpy = depth_extractor._zoe.infer_pil(image)  # as numpy
    depth_pil = depth_extractor._zoe.infer_pil(image, output_type="pil")  # as 16-bit PIL Image
    depth_tensor = depth_extractor._zoe.infer_pil(image, output_type="tensor")  # as torch tensor
    X = pil_to_batched_tensor(image).to(DEVICE)
    depth_tensor = depth_extractor._zoe.infer(X)
    depth = depth_extractor._zoe.infer_pil(image)
    print(depth_numpy)
