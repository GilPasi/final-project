
import os 
import numpy as np 
import pickle
import subprocess
import matplotlib.pyplot as plt
import threading
import queue

from PIL import Image
from width_estimating import multiple_normalize_object_width
from utils import get_algorithm_dir,ipc_file_path, SNAPSHOT_SIZE
from cropping import glue_map, crop_prediction

def get_predictions():
    segmentor_script_path = os.path.join(get_algorithm_dir(), "segmentor.py")
    depth_extractor_script_path = os.path.join(get_algorithm_dir(), "depth_extractor.py")

    SEGMENTATION_ENVIRONMENT = "segenv"
    DEPTH_EXTRACTING_ENVIRONMENT = "zoe"
    
    seg_output = queue.Queue()
    dep_output = queue.Queue()

    seg_thread = threading.Thread(
        target=predict_with_venv, 
        args=(segmentor_script_path, SEGMENTATION_ENVIRONMENT, seg_output))
    
    dep_thread = threading.Thread(
        target=predict_with_venv, 
        args=(depth_extractor_script_path, DEPTH_EXTRACTING_ENVIRONMENT, dep_output))
    
    seg_thread.start()
    dep_thread.start()

    seg_thread.join()
    dep_thread.join()

    seg_prediction = seg_output.get()
    dep_prediction = dep_output.get()
    return seg_prediction,dep_prediction


def predict_with_venv(script_path: str, env_name: str, output_queue: queue):
    command = f"conda run -n {env_name} python {script_path}"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    if process.returncode != 0:
        raise Exception("Subprocess failed to execute properly", process.stderr)
    else:
        with open(ipc_file_path(env_name), 'rb') as file:
            prediction = pickle.load(file)
        os.remove(ipc_file_path(env_name))
        output_queue.put(prediction)
    


def _present_results(depth_sample = None, segmentation_sample = None,
                    combined_sample = None, image_path = None):
    if image_path is not None: 
        img = Image.open(image_path)
        img_resized = img.resize(SNAPSHOT_SIZE)  
        img_array = np.array(img_resized)

    fig, axs = plt.subplots(2, 2, figsize=(7, 7)) 
    if depth_sample is not None: 
        axs[0, 0].imshow(depth_sample, cmap='gray')
        axs[0, 0].set_title('Depth Analysis')
        axs[0, 0].axis('off')
    if segmentation_sample is not None:
        axs[0, 1].imshow(segmentation_sample, cmap='gray')
        axs[0, 1].set_title('Segmentation')
        axs[0, 1].axis('off')

    if combined_sample is not None:
        axs[1, 0].imshow(combined_sample, cmap='gray')
        axs[1, 0].set_title('Combined Representation')
        axs[1, 0].axis('off')

    if image_path is not None: 
        axs[1, 1].imshow(img_array, cmap='gray')
        axs[1, 1].set_title('Original Input')
        axs[1, 1].axis('off')

    plt.tight_layout()  
    plt.show()

def _present_image(array_to_plot: np.ndarray, array_name:str = "Image"):
    plt.imshow(array_to_plot)
    plt.axis('off')  # Turn off the axis
    plt.title(array_name)  # Add a title to the image
    plt.show()
    
def _get_orientations():
    # Mockaup
    return ['vertical','vertical','vertical','vertical'] 

def produce_map():
    seg_prediction, dep_prediction = get_predictions()
    assert type(seg_prediction) == type(dep_prediction)
    assert np.shape(seg_prediction) == np.shape(dep_prediction),\
        f"seg shape {np.shape(seg_prediction)} is different than dep shape {np.shape(dep_prediction)}"
    combined_prediction = seg_prediction  * dep_prediction
    
    cropped_preds = crop_prediction(combined_prediction)    
    normal_results = multiple_normalize_object_width(cropped_preds)
    map = glue_map(normal_results, _get_orientations())

    _present_image(map)
    input("Press enter\n")
    return map

produce_map()


    


