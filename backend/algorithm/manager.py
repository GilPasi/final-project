
# segenv environment
import os 
import numpy as np 
import pickle
import subprocess

from utils import get_algorithm_dir
from utils import ipc_file_path

def parallel_predict(script_path, env_name):
    command = f"conda run -n {env_name} python {script_path}"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    if process.returncode != 0:
        raise Exception("Subprocess failed to execute properly", process.stderr)
    else:
        with open(ipc_file_path(env_name), 'rb') as file:
            prediction = pickle.load(file)
        os.remove(ipc_file_path(env_name))
        return prediction 
    
    


def main ():
    image_path = "1.png"

    segmentor_script_path = os.path.join(get_algorithm_dir(), "segmentor.py")
    depth_extractor_script_path = os.path.join(get_algorithm_dir(), "depth_extractor.py")

    SEGMENTATION_ENVIRONMENT = "segenv"
    DEPTH_EXTRACTING_ENVIRONMENT = "zoe"

    seg_prediction = parallel_predict(segmentor_script_path, SEGMENTATION_ENVIRONMENT)
    dep_prediction = parallel_predict(depth_extractor_script_path, DEPTH_EXTRACTING_ENVIRONMENT)

    assert type(seg_prediction) == type(dep_prediction)
    assert np.shape(seg_prediction) == np.shape(dep_prediction),\
        f"seg shape {np.shape(seg_prediction)} is different than dep shape {np.shape(dep_prediction)}"
    print("SUCCESS")

if __name__ == "__main__":
    main()





    


