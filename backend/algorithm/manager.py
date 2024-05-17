
# segenv environment
import os 
import numpy as np 
import os
os.environ["SM_FRAMEWORK"] = "tf.keras"
import segmentation_models as sm
import keras
import cv2
import matplotlib.pyplot as plt
from focal_loss import BinaryFocalLoss
from tensorflow.keras.models import load_model
from pathlib import Path
from depth_extractor import DepthExtractor
from segmentor import Segmentor


def main ():

    image_path = "/Users/gilpasi/Desktop/study/year-3/final-project/project/mappify/backend/algorithm/input/1.png"

    seg_analyser = Segmentor()
    dep_analysr = DepthExtractor()

    seg_prediction = seg_analyser.predict(image_path)
    dep_prediction = dep_analysr.predict(image_path)
    assert type(seg_analyser) == type(dep_analysr)
    assert np.shape(seg_prediction)==np.shape(dep_prediction),"seg shape is different than dep shape"
    print("SUCCESS")



    


