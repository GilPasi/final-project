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
 
class DepthExtractor(): 
    _zoe_instance = None

    def __init__(self):
        self._conf = get_config("zoedepth", "infer")
        model_zoe_n = DepthExtractor._get_zoe_instance()
        proccessing_unit = self._current_machine_pu()
        self._zoe = model_zoe_n.to(proccessing_unit)

        self.input_path = "cv_labratory/depth_analysis_lab/input" # Default, expected to change after the server is set
    
    @classmethod
    def _get_zoe_instance(cls):
        conf = get_config("zoedepth", "infer")
        if cls._zoe_instance is None:
            cls._zoe_instance = build_model(conf)
        return cls._zoe_instance
        
    def _current_machine_pu(self):
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _load_image(self, image_relative_path: str):
        mappify_path = _get_mappify_root_dir()
        absolute_image_path = os.path.join(mappify_path, image_relative_path)
        image = Image.open(absolute_image_path).convert("RGB")
        return image
    
    def predict(self, image_path: str):
        is_absolute_path = os.path.exists(image_path)
        if not is_absolute_path:
            image_path = os.path.join(self.input_path, image_path)
        if not os.path.exists(image_path): 
            raise ValueError("The given image path{image_path} is"
                             " neither absolute nor a valid image\n "
                             "name in the directory {self.imput_path}."
                             "Try to re-configure the image path or use an absoulte path.")
        image = self._load_image(image_path)
        return depth_extractor._zoe.infer_pil(image)

    def _save_product(self, depth, image_name, output_relative_path="cv_labratory/depth_analysis_lab/output/"):
        from zoedepth.utils.misc import save_raw_16bit
        from zoedepth.utils.misc import colorize
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
    depth_extractor = DepthExtractor()
    depth_numpy = depth_extractor.predict("1.png") 
    print(depth_numpy)


    # Additional capabilites of ZoeDepth for a potential development
    # depth_pil = depth_extractor._zoe.infer_pil(image, output_type="pil")  # as 16-bit PIL Image
    # depth_tensor = depth_extractor._zoe.infer_pil(image, output_type="tensor")  # as torch tensor
    # X = pil_to_batched_tensor(image).to(DEVICE)
    # depth_tensor = depth_extractor._zoe.infer(X)
