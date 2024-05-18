import os 
os.environ["SM_FRAMEWORK"] = "tf.keras"
import segmentation_models as sm
import numpy as np 
import keras
import cv2
import matplotlib.pyplot as plt
import sys
import pickle

from utils import infer_absolute_path
from utils import get_default_input_path
from utils import get_mappify_root_dir
from focal_loss import BinaryFocalLoss
from tensorflow.keras.models import load_model
from pathlib import Path

class Segmentor(): 
    _segmention_model_instance = None 

    def __init__(self):
        self.input_path = get_default_input_path() 
        self._model = Segmentor._get_segmentation_model_instance()
        self.threshhold = 0.07 # De facto works better for 0.07
        self.resize = (256, 256)
    
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

    def predict(self, image_path):
        image_path = infer_absolute_path(image_path, self.input_path) 
        single_image_array = self._load_images([image_path])
        prediction = self._model.predict(single_image_array)
        prediction = np.where(prediction > self.threshhold, 1, 0)
        return prediction

    def predict_multiple(self, samples_path):
        sample_data = self._load_images(samples_path)
        prediction = self._model.predict(sample_data)
        prediction = np.where(prediction > self.threshhold, 1, 0)
        return prediction
    
    def _load_images(self, images_paths: list):
        images = [self._load_image(path) for path in images_paths
                   if ".DS_Store" not in path]
        return np.array(images)

    
    def _load_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, self.resize)
        return image 

# For debugging
def plot_image_mask_result(mask):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(mask, cmap='gray')
    plt.show()

if __name__ == "__main__":
    segmentor = Segmentor()
    seg_prediction = segmentor.predict("1.png")
    serialized_data = pickle.dumps(seg_prediction)
    sys.stdout.buffer.write(serialized_data)
    # plot_image_mask_result(seg_prediction[0])
    # input("Press enter to exit\n")
