
# segenv environment
import os 
import numpy as np 
from depth_extractor import DepthExtractor
from segmentor import Segmentor

import subprocess

def parallel_predict(script_path, env_name, analyser):
    command = f"conda run -n {env_name} python {script_path}"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode == 0:
        print("Script output:", process.stdout)
    else:
        print("Error:", process.stderr)


def main ():
    image_path = "/Users/gilpasi/Desktop/study/year-3/final-project/project/mappify/backend/algorithm/input/1.png"

    seg_analyser = Segmentor()
    dep_analysr = DepthExtractor()

    seg_prediction = seg_analyser.predict(image_path)
    dep_prediction = dep_analysr.predict(image_path)


    # assert type(seg_analyser) == type(dep_analysr)
    # assert np.shape(seg_prediction)==np.shape(dep_prediction),"seg shape is different than dep shape"
    # print("SUCCESS")

if __name__ == "__main__":
    main()





    


