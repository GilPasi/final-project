import os 
os.environ["SM_FRAMEWORK"] = "tf.keras"
import segmentation_models as sm
import numpy as np 
import keras
import cv2
import matplotlib.pyplot as plt
import sys
import pickle

from utils import list_directory_contents
from utils import get_default_input_path
from utils import get_mappify_root_dir
from utils import ipc_file_path
from utils import SNAPSHOT_SIZE
from focal_loss import BinaryFocalLoss
from tensorflow.keras.models import load_model
from pathlib import Path
import logging



logging.basicConfig(filename='image_processing.log', 
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Segmentor(): 
    _segmention_model_instance = None 

    def __init__(self):
        self.input_path = get_default_input_path() 
        self._model = Segmentor._get_segmentation_model_instance()
        self.threshhold = 0.07 # De facto works better for 0.07
        self.threshhold = 0.5
    
    @classmethod
    def _get_segmentation_model_instance(cls):
        if cls._segmention_model_instance is None: 
            model = cls._recreate_model()
            cls._custom_compile(model)
            cls._segmention_model_instance = model
        return cls._segmention_model_instance
    
    @classmethod
    def _custom_compile(cls, model):
        metrics = [sm.metrics.IOUScore(threshold=0.5), sm.metrics.FScore(threshold=0.5)]
        model.compile('Adam', loss=BinaryFocalLoss(gamma=2), metrics=metrics)

    @classmethod
    def _recreate_model(cls):
        root_dir = get_mappify_root_dir()
        model_path = os.path.join( root_dir, "backend", "algorithm", "segmentor", "model.keras")
        model = load_model(model_path, compile=False)
        cls._custom_compile(model)
        return model

    def predict(self):
        sample_data = self._load_images()
        prediction = self._model.predict(sample_data)
        prediction = np.where(prediction > self.threshhold, 1, 0)
        prediction = np.squeeze(prediction)
        ARRAY_OF_IMAGES_DIMENSION = 3 
        if len(prediction.shape) != ARRAY_OF_IMAGES_DIMENSION:
            prediction = np.expand_dims(prediction, axis=0)

        return prediction
    
    def _load_images(self, all_images_paths: list = []):
        if all_images_paths == []:
            all_images_paths = list_directory_contents(
                self.input_path, allowed_extentsions=[".png", ".jpeg", ".jpg"])
        all_images = [self._load_image(img) for img in all_images_paths]
        return np.array(all_images)

    
    def _load_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, SNAPSHOT_SIZE)

        return image 

# For debugging
def plot_image_mask_result(mask1, mask2, mask3):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(10, 5))
    axs[0].imshow(mask1, cmap='gray')
    axs[1].imshow(mask2, cmap='gray')
    axs[2].imshow(mask3, cmap='gray')
    plt.show()

if __name__ == "__main__":
    ENVIRONMENT_NAME = "segenv"
    segmentor = Segmentor()
    seg_prediction = segmentor.predict()
    with open(ipc_file_path(ENVIRONMENT_NAME), 'wb') as file:
        pickle.dump(seg_prediction, file)

    # plot_image_mask_result(seg_prediction[0],seg_prediction[1], seg_prediction[2])
    # input("Press enter to exit\n")
