
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
# from Algorithm.depth_extractor import predict






def main ():
    samples_path = get_samples_path()
    model = restore_model()
    seg_prediction = predict_segmentation(model, samples_path)
    print(np.shape(seg_prediction))
    # depth_prediction = predict_depth(samples_path)


    # assert np.shape(seg_prediction)==np.shape(depth_prediction),"seg shape is different than dep shape"
    print("SUCCESS")



    


