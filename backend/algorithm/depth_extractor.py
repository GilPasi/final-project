import torch 
import sys
import os
import pickle
import numpy as np
from PIL import Image
from algorithm.utilities.administation import \
    get_mappify_root_dir,\
    get_default_input_path,\
    ipc_file_path,\
    SNAPSHOT_SIZE,\
    list_directory_contents
zoe_directory = os.path.join(get_mappify_root_dir(),"backend", "lib", "ZoeDepth")
sys.path.append(zoe_directory)
from algorithm.utilities.log_management import configure_logger

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
        self.logger = configure_logger(log_to_console=True, log_level="DEBUG")
    
    @classmethod
    def _get_zoe_instance(cls):
        conf = get_config("zoedepth", "infer")
        if cls._zoe_instance is None:
            cls._zoe_instance = build_model(conf)
        return cls._zoe_instance
        
    def _current_machine_pu(self):
        return "cuda" if torch.cuda.is_available() else "cpu"
    

    def _load_images(self, all_images_paths: list = []):
        if all_images_paths == []:
            all_images_paths = list_directory_contents(
                self.input_path, allowed_extentsions=[".png", ".jpeg", ".jpg"])
        mappify_path = get_mappify_root_dir()
        return [
            Image
                .open(os.path.join(mappify_path, image_path))
                .convert("RGB")
                .resize(SNAPSHOT_SIZE) 
            for image_path in all_images_paths
        ]
    
    def predict(self):
        images = self._load_images()
        self.logger.debug(f"images, {images}")

        all_predictions = [self._zoe.infer_pil(img) for img in images]
        self.logger.debug(f"preds {all_predictions[0].shape}", )

        return np.array(all_predictions)

    def _save_product(self, depth, image_name, output_relative_path="cv_labratory/depth_analysis_lab/output/"):
        from zoedepth.utils.misc import save_raw_16bit
        from zoedepth.utils.misc import colorize

        colored_image_name = "colored_" + image_name
        mappify_path = get_mappify_root_dir()
        absolute_output_path = os.path.join(
            mappify_path, output_relative_path, image_name)
        absolute_colored_output_path = os.path.join(
            mappify_path, output_relative_path, colored_image_name)
        save_raw_16bit(depth, absolute_output_path)
        colored = colorize(depth)
        Image.fromarray(colored).save(absolute_colored_output_path)

if __name__ == "__main__":
    ENVIRONMENT_NAME = "zoe"
    segmentor = DepthExtractor()
    dep_prediction = segmentor.predict()
    with open(ipc_file_path(ENVIRONMENT_NAME), 'wb') as file:
        pickle.dump(dep_prediction, file)


    # ____Additional capabilites of ZoeDepth for a potential development_____
    # depth_pil = depth_extractor._zoe.infer_pil(image, output_type="pil")  # as 16-bit PIL Image
    # depth_tensor = depth_extractor._zoe.infer_pil(image, output_type="tensor")  # as torch tensor
    # X = pil_to_batched_tensor(image).to(DEVICE)
    # depth_tensor = depth_extractor._zoe.infer(X)
