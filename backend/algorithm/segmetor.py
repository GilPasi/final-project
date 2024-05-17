import os 
os.environ["SM_FRAMEWORK"] = "tf.keras"
import segmentation_models as sm
import numpy as np 
import keras
import cv2
import matplotlib.pyplot as plt

from focal_loss import BinaryFocalLoss
from tensorflow.keras.models import load_model
from pathlib import Path

class Segmentor(): 
    _segmention_model_instance = None 

    def __init__(self):
        self.input_path = "cv_labratory/depth_analysis_lab/input" # Default, expected to change after the server is set
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

# TODO: remove the segmentor to inside of the package
    @classmethod
    def _recreate_model(cls):
        LAB_PATH = os.getcwd()
        MODEL_NAME = "road_segmentor"
        MODEL_PATH = os.path.join(LAB_PATH,"cv_labratory",
                "segmentation_lab","products", MODEL_NAME,"model.keras" )
        model = load_model(MODEL_PATH,compile=False)
        cls._custom_compile(model)
        return model
        

    def predict(self, image_path):
        # TODO: remove code duplications with zoe
        is_absolute_path = os.path.exists(image_path)
        if not is_absolute_path:
            image_path = os.path.join(self.input_path, image_path)
        if not os.path.exists(image_path): 
            raise ValueError("The given image path{image_path} is"
                             " neither absolute nor a valid image\n "
                             "name in the directory {self.imput_path}.") 
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
    seg_prediction = segmentor.predict("/Users/gilpasi/Desktop/study/year-3/final-project/project/mappify/cv_labratory/depth_analysis_lab/input/1.png")
    print(np.shape(seg_prediction))
    print(seg_prediction)
    plot_image_mask_result(seg_prediction[0])
