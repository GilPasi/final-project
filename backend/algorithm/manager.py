
# segenv environment
import os 
import numpy as np 
import pickle
from depth_extractor import DepthExtractor
from segmentor import Segmentor

import subprocess

def parallel_predict(script_path, env_name):
    command = f"conda run -n {env_name} python {script_path}"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    prediction = pickle.loads(process.stdout)

    if process.returncode == 0:
        return prediction
    else:
        raise Exception (f"Error: something went wrong with "
                         f"{script_path} and environment {env_name},"
                         f"{process.stderr}")


def main ():
    image_path = "1.png"

    seg_analyser = Segmentor()
    # dep_analysr = DepthExtractor()

    seg_prediction = seg_analyser.predict(image_path)
    # dep_prediction = dep_analysr.predict(image_path)


    # assert type(seg_analyser) == type(dep_analysr)
    # assert np.shape(seg_prediction)==np.shape(dep_prediction),"seg shape is different than dep shape"
    # print("SUCCESS")

if __name__ == "__main__":
    main()





    


