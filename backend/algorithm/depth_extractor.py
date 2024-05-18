import torch 
import sys
import os
import pickle

from PIL import Image
from utils import infer_absolute_path
from utils import get_mappify_root_dir
from utils import get_default_input_path
from utils import ipc_file_path
from utils import SNAPSHOT_SIZE
zoe_directory = os.path.join(get_mappify_root_dir(),"backend", "lib", "ZoeDepth")
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
        self.input_path = get_default_input_path()
    
    @classmethod
    def _get_zoe_instance(cls):
        conf = get_config("zoedepth", "infer")
        if cls._zoe_instance is None:
            cls._zoe_instance = build_model(conf)
        return cls._zoe_instance
        
    def _current_machine_pu(self):
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _load_image(self, image_relative_path: str):
        mappify_path = get_mappify_root_dir()
        absolute_image_path = os.path.join(mappify_path, image_relative_path)
        image = Image.open(absolute_image_path).convert("RGB")
        image = image.resize(SNAPSHOT_SIZE)
        return image
    
    def predict(self, image_path: str):
        image_path = infer_absolute_path(image_path, self.input_path) 
        image = self._load_image(image_path)
        return self._zoe.infer_pil(image)

    def _save_product(self, depth, image_name, output_relative_path="cv_labratory/depth_analysis_lab/output/"):
        from zoedepth.utils.misc import save_raw_16bit
        from zoedepth.utils.misc import colorize
        # This method is not actually required on production since there is no need to see the products.
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
    ENVIRONMENT_NAME = "zoe"
    segmentor = DepthExtractor()
    seg_prediction = segmentor.predict("1.png")
    with open(ipc_file_path(ENVIRONMENT_NAME), 'wb') as file:
        pickle.dump(seg_prediction, file)


    # ____Additional capabilites of ZoeDepth for a potential development_____
    # depth_pil = depth_extractor._zoe.infer_pil(image, output_type="pil")  # as 16-bit PIL Image
    # depth_tensor = depth_extractor._zoe.infer_pil(image, output_type="tensor")  # as torch tensor
    # X = pil_to_batched_tensor(image).to(DEVICE)
    # depth_tensor = depth_extractor._zoe.infer(X)
