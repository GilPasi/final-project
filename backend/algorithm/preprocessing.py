import cv2

from algorithm.utilities.image_utils import \
    take_video_snapshots,\
    take_gyroscope_snapshots,\
    processing_cleanup ,\
    save_pictures, \
    in_memory_video_to_video_capture\

from algorithm.utilities.administation import get_default_input_path
from algorithm.exceptions.unsynced_crude_data_exception import UnsyncedCrudeDataException
from algorithm.utilities.log_management import configure_logger
logger = configure_logger(log_to_console=True, log_level='DEBUG')

def take_snapshots(video, gyroscope_data,snapshot_interval = 3 ):
    visual_snapshots = take_video_snapshots(video, snapshot_interval)
    gyroscope_snapshots = take_gyroscope_snapshots(gyroscope_data, snapshot_interval)
    return visual_snapshots, gyroscope_snapshots

def straighten_gyroscope_data(video, gyroscope_data):
    video_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    gyroscope_data_frame_count = len(gyroscope_data)
    prepared_gyroscope_data = [] 

    logger.debug(f"Video frames count {video_frame_count}")
    logger.debug(f"Video frames count {gyroscope_data_frame_count}")

    DEVIATION_THRESHHOLD = 0.2 # If there is an unsynchronization of more than 20% raise an exception
    if not 1 - DEVIATION_THRESHHOLD <\
          gyroscope_data_frame_count / video_frame_count < 1 + DEVIATION_THRESHHOLD :
        raise UnsyncedCrudeDataException(DEVIATION_THRESHHOLD, None,
            ("video" ,video_frame_count),("gyroscope data", gyroscope_data_frame_count) )
    

    if gyroscope_data_frame_count > video_frame_count: 
        gyroscope_data_delta_from_video_frame_count= len(gyroscope_data) - video_frame_count
        prepared_gyroscope_data = gyroscope_data[gyroscope_data_delta_from_video_frame_count // 2 :
                                                - gyroscope_data_delta_from_video_frame_count // 2]

    if gyroscope_data_frame_count < video_frame_count: 
        total_padding = video_frame_count - gyroscope_data_frame_count
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        first_cell = gyroscope_data[0]
        last_cell = gyroscope_data[-1]
        prepared_gyroscope_data = [first_cell] * left_padding + gyroscope_data + [last_cell] * right_padding
    
    return prepared_gyroscope_data

def preprocess(video_file, gyroscope_data:list,):
    processing_cleanup(get_default_input_path())
    video_instance = in_memory_video_to_video_capture(video_file)
    # Straithen only the gyroscope since straightening the video is way more complex
    # and anyway will be implemented in the client's proxy in the future.
    prepared_gyroscope_data  = straighten_gyroscope_data(video_instance, gyroscope_data)  
    visual_snapshots, gyroscope_snapshots = take_snapshots(video_instance, prepared_gyroscope_data)
    video_instance.release()
    save_pictures(visual_snapshots,get_default_input_path())
    return _get_orientations(gyroscope_snapshots)


def _get_orientations(gyroscope_snapshots: list):
    # Mockaup
    # print ""
    orientations = ['vertical'] * len(gyroscope_snapshots)
    return orientations