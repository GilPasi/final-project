
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
from backend.Algorithm.depth_extractor import produce_zoe, load_image



def custom_compile(model):
    metrics = [sm.metrics.IOUScore(threshold=0.5), sm.metrics.FScore(threshold=0.5)]
    model.compile('Adam', loss=BinaryFocalLoss(gamma=2), metrics=metrics)


def get_images_absolute_paths(base_dir):
    return sorted([str(file)
                   for file in Path(base_dir).iterdir()
                   if file.is_file()])

def load_images(image_paths):
    RESIZE = (256, 256)
    images = []
    for path in image_paths:
        if ".DS_Store" not in path: 
            img = cv2.imread(path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, RESIZE)
            images.append(img)
    return np.array(images)

def plot_image_mask_result(x, y, z=None):
    fig, axs = plt.subplots(1, 3, figsize=(10, 5))
    axs[0].imshow(x)
    axs[1].imshow(y, cmap='gray')
    axs[2].imshow( np.zeros(x.shape) if z is None else z, cmap='gray')
    plt.show()

def predict_segmentation(model, samples_path):
    sample_data = load_images(samples_path)
    THRESHOLD = 0.07 # De facto works better for 0.07
    prediction = model.predict(sample_data)
    prediction = np.where(prediction > THRESHOLD, 1, 0)
    return prediction

    # for i in range(len(sample_data)):
    #     plot_image_mask_result(sample_data[i],prediction[i])

def get_samples_path():
    sample_dir_path = os.path.join(
        os.getcwd(), 'cv_labratory', 'segmentation_lab'
        , 'datasets', 'google-maps-sample')
    samples_path = get_images_absolute_paths(sample_dir_path)
    return samples_path

def restore_model():
    LAB_PATH = os.getcwd()
    MODEL_NAME = "road_segmentor"
    MODEL_PATH = os.path.join(LAB_PATH,"cv_labratory",
            "segmentation_lab","products", MODEL_NAME,"model.keras" )
    model = load_model(MODEL_PATH,compile=False)
    custom_compile(model)
    return model

def predict_depth(samples_path: list):
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    zoe = produce_zoe(DEVICE)
    images = [zoe.infer_pil(load_image(img)) for img in samples_path] 
    return images

def main ():
    samples_path = get_samples_path()

    model = restore_model()
    seg_prediction = predict_segmentation(model, samples_path)
    depth_prediction = predict_depth(samples_path)

    
    assert np.shape(seg_prediction)==np.shape(depth_prediction),"seg shape is different than dep shape"
    print("SUCCESS")


if __name__ == "__main__": 
    main()

    


