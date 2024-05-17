
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

    # assert np.shape(seg_prediction)==np.shape(depth_prediction),"seg shape is different than dep shape"
    print("SUCCESS")



    


