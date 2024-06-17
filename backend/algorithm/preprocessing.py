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

def preprocess(video_file, gyroscope_data:list,):
    processing_cleanup(get_default_input_path())
    video_instance = in_memory_video_to_video_capture(video_file)
    # Straigthen only the gyroscope since straightening the video is way more complex
    # and anyway will be implemented in the client's proxy in the future.
    prepared_gyroscope_data = straighten_gyroscope_data(video_instance, gyroscope_data)  
    visual_snapshots, gyroscope_snapshots = take_snapshots(video_instance, prepared_gyroscope_data)
    video_instance.release()
    save_pictures(visual_snapshots,get_default_input_path())
    return _get_orientations(gyroscope_snapshots)


def _get_orientations(gyroscope_snapshots: list):
    result = None
    current_state = {
        'facing': 0,
        'x' : 0, 
        'y' : 0,
    }
    rotation_axis = _extract_rotation_axis(gyroscope_snapshots)
    
    for index, rot_value in enumerate(rotation_axis):
        logger.debug("Gyroscope y " + str(rotation_axis))

        if result is None: 
            result = np.ndarray([(index, current_state['facing'])])
        
        else:
            current_state['facing'] = _evaluate_new_facing(current_state['facing'], rot_value)
            current_state = _pump_matrix_with_walker(result, current_state)
            


        


        
        

        


    #TODO: relate
    # if len(matrices) != len(orientations):
    # raise ValueError(f"The number of matrices ({len(matrices)}) " + 
    #                     f"and orientations count ({len(orientations)}) must be the same.")

        
    orientations.append(directions[current_facing])
    logger.debug("Orientations " + str(orientations))
    return orientations

    result = matrices[0]
    for i in range(1, len(matrices)):
        logger.debug("Current orientation " +  orientations[i])
        if orientations[i] == 'left':
            rotated_matix = np.rot90(matrices[i], k=1)
            target_shape = (result.shape[0], result.shape[1] + rotated_matix.shape[1])
            logger.debug(f"target_shape is {target_shape}")
            padded_matrix = pad_matrix(rotated_matix, target_shape, 'left')
            padded_result = pad_matrix(result, target_shape, 'right')
            result = np.hstack((padded_matrix, padded_result))

        elif orientations[i] == 'right':
            rotated_matix = np.rot90(matrices[i], k=-1)
            target_shape = (result.shape[0], result.shape[1] + rotated_matix.shape[1])
            logger.debug(f"target_shape is {target_shape}")
            padded_matrix = pad_matrix(rotated_matix, target_shape, 'right')
            padded_result = pad_matrix(result, target_shape, 'right')
            result = np.hstack((padded_result, padded_matrix))

        elif orientations[i] == 'forward':
            target_shape = (result.shape[0] + matrices[i].shape[0], result.shape[1])
            padded_matrix = pad_matrix(matrices[i], target_shape, 'forward')
            padded_result = pad_matrix(result, target_shape, 'forward')
            result = np.vstack((padded_matrix, padded_result))
        else:
            raise ValueError("Invalid orientation. Use one of the following: 'forward', 'left', 'right' .")
    
    return result

def _pump_matrix_with_walker(matrix: np.ndarray, walker_state: dict):

    """
    Expand a matrix to it's width or height according to a walker's state. 
    A walker represent the person who is walking the space and require the map to expand
    to match his walk.

    Parameters: 
    matrix         (np.ndarray): matrix of already explored files where matrix.ndim == 2
    walker_state   (dict): Dictionary to describe the walker's condition in the form 
                        {'facing': <value: int in range [1,4]>,
                          'x': <value: int in range [0,inf]> ,'y': <value: int in range [0,inf]>} 

    Returns: 
    result          (tuple): Both the pumped matrix and the new state after making the walker's move.                          
    """

    NORTH = 0
    EAST = 1 
    SOUTH = 2
    WEST = 3

    if walker_state['facing'] == NORTH:
        new_row = np.zeros((1, matrix.shape[1]))
        matrix = np.vstack((new_row, matrix))
        walker_state['y'] += 1

    elif walker_state['facing'] == EAST:
        new_col = np.zeros((matrix.shape[0], 1))
        matrix = np.hstack((matrix, new_col))
        walker_state['x'] += 1

    elif walker_state['facing'] == SOUTH:
        new_row = np.zeros((1, matrix.shape[1]))
        matrix = np.vstack((matrix, new_row))
        walker_state['y'] -= 1

    elif walker_state['facing'] == WEST:
        new_col = np.zeros((matrix.shape[0], 1))
        matrix = np.hstack((new_col, matrix))
        walker_state['x'] -= 1
        
    return matrix, walker_state


def _evaluate_new_facing(current_facing, rot_value):
        rotation_threshhold = 1 
        if rot_value < -rotation_threshhold:
            current_facing -= 1
        elif rot_value > rotation_threshhold:
            current_facing += 1


def _extract_rotation_axis(gyroscope_data:list):
    """
    Filter only the relevant axis for infering where the user faced while filming
    
    Parameters:
    gyroscope_data  (list): list of dictionaries in the form 
        {'x': <xval: decimal>, 'y': <yval: decimal>, 'z': <zval: decimal>}

    Returns: 
    result  (list): list of only the relevant values with no keys in the form [<val1:decimal>,<val2:decimal> ... ] 
    """
    return [data_snapshot['y'] for data_snapshot in gyroscope_data if 'y' in data_snapshot]