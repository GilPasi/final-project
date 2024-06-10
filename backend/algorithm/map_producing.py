import os 
import numpy as np 
import pickle
import subprocess
import matplotlib.pyplot as plt
import threading
import queue
import sys 
import cv2

    
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..',))
sys.path.append(parent_dir)

from PIL import Image
from algorithm.width_estimating import multiple_normalize_object_width
from algorithm.exceptions.unsynced_crude_data_exception import UnsyncedCrudeDataException
from algorithm.utils import \
    get_algorithm_dir,\
    ipc_file_path,\
    SNAPSHOT_SIZE,\
    get_default_input_path,\
    count_items_in_path\

from algorithm.image_utils import \
    glue_map,\
    crop_prediction,\
    take_video_snapshots,\
    take_gyroscope_snapshots,\
    processing_cleanup ,\
    save_pictures, \
    in_memory_video_to_video_capture\
    
from algorithm.log_management import configure_logger
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

    logger.info("Prediction process is complete")

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
    
def _get_orientations(gyroscope_snapshots: list):
    # Mockaup
    orientations = ['vertical'] * len(gyroscope_snapshots)
    return orientations

def combine_analysis(dep_prediction, seg_prediction):
    return dep_prediction * seg_prediction

def process_predictions(seg_prediction, dep_prediction):
    combined_prediction = combine_analysis(seg_prediction, dep_prediction)
    cropped_preds = crop_prediction(combined_prediction)    
    normal_results = multiple_normalize_object_width(cropped_preds)
    return normal_results

def take_snapshots(video, gyroscope_data,snapshot_interval = 3 ):
    visual_snapshots = take_video_snapshots(video, snapshot_interval)
    gyroscope_snapshots = take_gyroscope_snapshots(gyroscope_data, snapshot_interval)
    return visual_snapshots, gyroscope_snapshots

def straighten_gyroscope_data(video, gyroscope_data):
    video_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    gyroscope_data_frame_count = len(gyroscope_data)
    prepared_gyroscope_data = [] 
    print("gyro vector, ", gyroscope_data_frame_count)
    print("cam vector,", video_frame_count )

    min_frame_count = min(video_frame_count, gyroscope_data_frame_count)
    logger.debug(f"Video frames count {video_frame_count}")
    logger.debug(f"Video frames count {gyroscope_data_frame_count}")

    DEVIATION_THRESHHOLD = 1.2 # If there is an unsynchronization of more than 20% raise an exception

    if video_frame_count / min_frame_count > DEVIATION_THRESHHOLD or \
        gyroscope_data_frame_count / min_frame_count > DEVIATION_THRESHHOLD:
        raise UnsyncedCrudeDataException(
            DEVIATION_THRESHHOLD, None, ("video" ,video_frame_count), ("gyroscope data", gyroscope_data_frame_count) )
    
    if gyroscope_data_frame_count > min_frame_count:  
        gyroscope_data_delta_from_from_minimum = len(gyroscope_data) - min_frame_count
        prepared_gyroscope_data = gyroscope_data[gyroscope_data_delta_from_from_minimum // 2 :
                                                - gyroscope_data_delta_from_from_minimum // 2]

    if gyroscope_data_frame_count < min_frame_count: 
        total_padding = min_frame_count - gyroscope_data_frame_count
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        first_cell = gyroscope_data[0]
        last_cell = gyroscope_data[-1]
        prepared_gyroscope_data = [first_cell] * left_padding + gyroscope_data + [last_cell] * right_padding
    
    print("Prepared gyroscop fc," , len(prepared_gyroscope_data))
    return prepared_gyroscope_data

def preprocess(video_file, gyroscope_data:list,):
    processing_cleanup(get_default_input_path())
    video_instance = in_memory_video_to_video_capture(video_file)
    # Straithen only the gyroscope since straithening the video is way more complex
    # and any way will be implemented in the client's proxy in the future.

    prepared_gyroscope_data  = straighten_gyroscope_data(video_instance, gyroscope_data)
    visual_snapshots, gyroscope_snapshots = take_snapshots(video_instance, prepared_gyroscope_data)
    video_instance.release()
    save_pictures(visual_snapshots,get_default_input_path())
    return _get_orientations(gyroscope_snapshots)

def produce_map(video_file, gyroscope_data:list, debug = False):
    logger.info("Preprocessing start")
    orientations = preprocess(video_file, gyroscope_data)

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
