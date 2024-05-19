
# segenv environment
import os 
import numpy as np 
import pickle
import subprocess
import matplotlib.pyplot as plt
from PIL import Image
import threading
import queue

from utils import get_algorithm_dir,ipc_file_path, SNAPSHOT_SIZE

def parallel_predict(script_path: str, env_name: str, output_queue: queue):
    command = f"conda run -n {env_name} python {script_path}"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    if process.returncode != 0:
        raise Exception("Subprocess failed to execute properly", process.stderr)
    else:
        with open(ipc_file_path(env_name), 'rb') as file:
            prediction = pickle.load(file)
        os.remove(ipc_file_path(env_name))
        output_queue.put(prediction)
    


def _present_image(depth_sample, segmentation_sample,
                    combined_sample, image_path):
    
    img = Image.open(image_path)
    img_resized = img.resize(SNAPSHOT_SIZE)  
    img_array = np.array(img_resized)

    fig, axs = plt.subplots(2, 2, figsize=(7, 7)) 

    axs[0, 0].imshow(depth_sample, cmap='gray')
    axs[0, 0].set_title('Depth Analysis')
    axs[0, 0].axis('off')

    axs[0, 1].imshow(segmentation_sample, cmap='gray')
    axs[0, 1].set_title('Segmentation')
    axs[0, 1].axis('off')

    axs[1, 0].imshow(combined_sample, cmap='gray')
    axs[1, 0].set_title('Conbined Representation')
    axs[1, 0].axis('off')

    axs[1, 1].imshow(img_array, cmap='gray')
    axs[1, 1].set_title('Original Input')
    axs[1, 1].axis('off')

    plt.tight_layout()  
    plt.show()


def get_predictions():
    segmentor_script_path = os.path.join(get_algorithm_dir(), "segmentor.py")
    depth_extractor_script_path = os.path.join(get_algorithm_dir(), "depth_extractor.py")

    SEGMENTATION_ENVIRONMENT = "segenv"
    DEPTH_EXTRACTING_ENVIRONMENT = "zoe"
    
    seg_output = queue.Queue()
    dep_output = queue.Queue()

    seg_thread = threading.Thread(
        target=parallel_predict, 
        args=(segmentor_script_path, SEGMENTATION_ENVIRONMENT, seg_output))
    
    dep_thread = threading.Thread(
        target=parallel_predict, 
        args=(depth_extractor_script_path, DEPTH_EXTRACTING_ENVIRONMENT, dep_output))
    
    seg_thread.start()
    dep_thread.start()

    seg_thread.join()
    dep_thread.join()

    seg_prediction = seg_output.get()
    dep_prediction = dep_output.get()
    return seg_prediction,dep_prediction


def main ():
    seg_prediction, dep_prediction = get_predictions()
    assert type(seg_prediction) == type(dep_prediction)
    assert np.shape(seg_prediction) == np.shape(dep_prediction),\
        f"seg shape {np.shape(seg_prediction)} is different than dep shape {np.shape(dep_prediction)}"
    combined_prediction = seg_prediction * dep_prediction
    _present_image(dep_prediction[0],seg_prediction[0],
                combined_prediction[0],"backend/algorithm/input/dog_walk_2.png")
    input("Press enter to exit \n ")


if __name__ == "__main__":
    main()

    


