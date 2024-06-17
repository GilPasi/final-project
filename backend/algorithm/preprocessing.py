import cv2
import numpy as np 

from algorithm.utilities.image_utils import \
    take_video_snapshots,\
    take_gyroscope_snapshots,\
    processing_cleanup ,\
    save_pictures, \
    in_memory_video_to_video_capture,\
    get_video_fps\

from algorithm.utilities.administation import get_default_input_path
from algorithm.exceptions.unsynced_crude_data_exception import UnsyncedCrudeDataException
from algorithm.utilities.log_management import configure_logger
logger = configure_logger(log_to_console=True, log_level='DEBUG')



def take_snapshots(video, gyroscope_data,snapshot_interval = 1):
    fps = get_video_fps(video)
    visual_snapshots = take_video_snapshots(video, snapshot_interval, fps)
    gyroscope_snapshots = take_gyroscope_snapshots(gyroscope_data, snapshot_interval, fps)
    if len(visual_snapshots) != len(gyroscope_snapshots) : 
        raise Exception("Unsuccessful snapshooting, video snapshots\
                        length {len(visual_snapshots)}, gyroscope snapshots\
                         length {len(gyroscope_snapshots)}")
    return visual_snapshots, gyroscope_snapshots

def straighten_gyroscope_data(video, gyroscope_data):
    video_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    gyroscope_data_frame_count = len(gyroscope_data)
    prepared_gyroscope_data = [] 

    logger.debug(f"Video frames count {video_frame_count}")
    logger.debug(f"Gyroscope frames count {gyroscope_data_frame_count}")

    DEVIATION_THRESHHOLD = 0.2 # If there is an unsynchronization of more than 20% raise an exception
    if not 1 - DEVIATION_THRESHHOLD <\
          gyroscope_data_frame_count / video_frame_count < 1 + DEVIATION_THRESHHOLD :
        raise UnsyncedCrudeDataException(DEVIATION_THRESHHOLD, None,
            ("video" ,video_frame_count),("gyroscope data", gyroscope_data_frame_count) )
    

    if gyroscope_data_frame_count > video_frame_count: 
        gyroscope_data_delta_from_video_frame_count = len(gyroscope_data) - video_frame_count
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


NORTH = 0
EAST = 1 
SOUTH = 2
WEST = 3 

def preprocess(video_file, gyroscope_data:list,):
    processing_cleanup(get_default_input_path())
    video_instance = in_memory_video_to_video_capture(video_file)
    # Straigthen only the gyroscope since straightening the video is way more complex
    # and anyway will be implemented in the client's proxy in the future.
    prepared_gyroscope_data = straighten_gyroscope_data(video_instance, gyroscope_data)  
    visual_snapshots, gyroscope_snapshots = take_snapshots(video_instance, prepared_gyroscope_data)
    video_instance.release()
    save_pictures(visual_snapshots, get_default_input_path())
    return _get_positions(gyroscope_snapshots)

def _get_positions(gyroscope_snapshots: list):
    rotation_axis = _extract_rotation_axis(gyroscope_snapshots)
    logger.debug(f"Original rotation axis {rotation_axis}")
    directions, directions_count = _evaluate_directions(rotation_axis)
    logger.debug(f"Found directions (N = 0, E = 1, S = 2, W = 3 ) {directions}, directions count {directions_count}")
    map_shape = _calculate_map_shape(directions_count)
    result = np.zeros(map_shape, dtype=object)
    logger.debug(f"Positions matrix created with shape {result.shape}")
    current_x, current_y = map_shape[1] // 2, map_shape[0] // 2 # Exact middle

    for idx, direction in enumerate(directions):
        try:
            result[current_y, current_x] = (idx, direction)
            current_x, current_y = _evaluate_new_position(current_x, current_y, direction)
        except Exception as ex: 
            logger.debug(f"Current x|y : {current_x}|{current_y}.")
            raise ex

    return result         

def _evaluate_new_position(x :int, y: int, direction: float):
    
    if direction == NORTH: y -= 1 
    elif direction == EAST: x += 1
    elif direction == SOUTH: y += 1 
    elif direction == WEST: x -= 1

    return x,y


def _extract_rotation_axis(gyroscope_data:list):
    """
    Filter only the relevant axis for infering where the user faced while filming
    
    Parameters:
    gyroscope_data  (list): list of dictionaries in the form 
        {'x': <xval: float>, 'y': <yval: float>, 'z': <zval: float>}

    Returns: 
    result  (list): list of only the relevant values with no keys in the form [<val1:float>,<val2:float> ... ] 
    """
    return [data_snapshot['y'] for data_snapshot in gyroscope_data if 'y' in data_snapshot]


def _evaluate_directions(gyroscope_rotations: list):
    current_direction = NORTH
    directions_count = [0,0,0,0] # (North, East, South, West)
    result = [] 

    for rot_value in gyroscope_rotations: 
        result.append(current_direction)
        directions_count[current_direction] += 1 
        current_direction = _evaluate_new_facing(current_direction, rot_value)

    return result, directions_count

def _evaluate_new_facing(current_facing, rot_value):
    FULL_CYCLE = 4 
    rotation_threshhold = 1 
    if rot_value < -rotation_threshhold:
        current_facing += 1
    elif rot_value > rotation_threshhold:
        current_facing -= 1
    return current_facing % FULL_CYCLE
        

def _calculate_map_shape(directions_count :tuple):
    """"
    Calculate the  minimal necessary dimensions to make the map without getting out of 
    bound issues. It might waste some space, but It will create an easier structure to maintain. 
    
    On the worst case the map cannot be any way wider than twice of the maximum step horizontally.

    It is important to ensure an odd width and height so the exact middle can be found easily.

    Parameters:     
    directions_count    (list): List that represent the count of each direction evaluated in the previous
        step.Should be in a form [<north: int>, <east: int>, <south: int>, <west: int>].

    Returns: 
    result              (tuple): Tuple with minmal width and height if the map.
        Should be in form (<height: odd int>, <width: odd int>)
    """

    SAFETY_MULTIPLIER = 2 
    height = max(directions_count[NORTH], directions_count[SOUTH]) * SAFETY_MULTIPLIER
    width = max(directions_count[EAST], directions_count[WEST]) * SAFETY_MULTIPLIER
    # Ensure odd: 
    height += (height + 1 ) % 2
    width += (width + 1 ) % 2

    return height, width


     
    