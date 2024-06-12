import os 
import numpy as np 
import pickle
import subprocess
import matplotlib.pyplot as plt
import threading
import queue
import sys 

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..',))
sys.path.append(parent_dir)

from PIL import Image
from algorithm.width_estimating import multiple_normalize_object_width
from algorithm.utilities.administation import \
    get_algorithm_dir,\
    ipc_file_path,\
    SNAPSHOT_SIZE\

from algorithm.utilities.image_utils import \
    glue_map,\
    crop_prediction\
    
from algorithm.preprocessing import preprocess
    
from algorithm.utilities.log_management import configure_logger
logger = configure_logger(log_to_console=True, log_level='DEBUG')

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
    logger.info(f"smart prediction with {env_name}")
    command = f"conda run -n {env_name} python {script_path}"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    if process.returncode != 0:
        raise Exception("Subprocess failed to execute properly", process.stderr)
    else:
        with open(ipc_file_path(env_name), 'rb') as file:
            prediction = pickle.load(file)
            logger.info("Data loaded from IPC successfully")
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
    plt.axis('off')
    plt.title(array_name)
    plt.show()
    
def combine_analysis(dep_prediction, seg_prediction):
    return dep_prediction * seg_prediction

def process_predictions(seg_prediction, dep_prediction):
    combined_prediction = combine_analysis(seg_prediction, dep_prediction)
    cropped_preds = crop_prediction(combined_prediction)    
    normal_results = multiple_normalize_object_width(cropped_preds)
    return normal_results

def produce_map(video_file, gyroscope_data:list, debug = False):
    logger.info("Preprocessing start")
    orientations = preprocess(video_file, gyroscope_data)
    logger.info("Start predicting")

    seg_prediction, dep_prediction = get_predictions()
    assert np.shape(seg_prediction) == np.shape(dep_prediction),\
        f"seg shape {np.shape(seg_prediction)} is different than dep shape {np.shape(dep_prediction)}"
    processed_output = process_predictions(seg_prediction, dep_prediction)

    logger.info("Glueing snapshots")
    map = glue_map(processed_output, orientations)
    if debug:
        try: # Do not let a mis-configuration make make the server collapse
            _present_image(map)
            input("Press enter\n")
        except:
            logger.error("Was not able to preview the results,"
                          "try to operate map_producing with no server on")

    return map
