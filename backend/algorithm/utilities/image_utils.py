import numpy as np
import cv2
import os
import shutil

from PIL import Image
from algorithm.utilities.administation import\
    list_directory_contents,\
    get_default_output_path,\
    prefix_from_absolute_path,\
    get_default_input_path,\
    slice_size,\
    MINIMUM_LIGHT_PIXELS_IN_LINE,\
    SNAPSHOT_SIZE
from algorithm.exceptions.damaged_snapshot_exception import DamagedSnapshotException
from tempfile import NamedTemporaryFile
from algorithm.utilities.log_management import configure_logger
logger = configure_logger(log_to_console=True, log_level='DEBUG')

def crop_image_to_square(image_path: str, output_path:str):
    image = Image.open(image_path)
    width, height = image.size
    min_dimension = min(width, height)

    left = (width - min_dimension) // 2
    top = (height - min_dimension) // 2
    right = left + min_dimension
    bottom = top + min_dimension
    cropped_image = image.crop((left, top, right, bottom))

    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    if not any(output_path.lower().endswith(ext) for ext in valid_extensions):
        raise ValueError(f"Invalid file extension in output path: {output_path}")
    cropped_image.save(output_path)

def find_first_positive_row(matrix, threshhold):
    positive_counts = np.sum(matrix > 0, axis=1)
    row_indices = np.where(positive_counts >= threshhold)[0]
    if row_indices.size > 0:
        return row_indices[0]
    else: 
        raise DamagedSnapshotException(f"The given matrix has too little light pixels" )

def pad_matrix(matrix, target_shape, orientation):
    """
    Pads the given matrix to the target shape with zeros.
    """
    pad_width = [(0, max(0, ts - ms)) for ms, ts in zip(matrix.shape, target_shape)]
    if orientation in ['left', 'right']:
        pad_width[1] = (0, 0)
    elif orientation == 'forward':
        pad_width[0] = (0, 0)
    
    return np.pad(matrix, pad_width, mode='constant')

def glue_map(matrices: list, orientations: list):
    if len(matrices) != len(orientations):
        raise ValueError(f"The number of matrices ({len(matrices)}) " + 
                         f"and orientations count ({len(orientations)}) must be the same.")
    
    result = matrices[0]
    for i in range(1, len(matrices)):
        if orientations[i] == 'left':
            target_shape = (result.shape[0], result.shape[1] + matrices[i].shape[1])
            padded_matrix = pad_matrix(matrices[i], target_shape, 'left')
            padded_result = pad_matrix(result, target_shape, 'right')
            result = np.hstack((padded_matrix, padded_result))

        elif orientations[i] == 'right':
            target_shape = (result.shape[0], result.shape[1] + matrices[i].shape[1])
            padded_matrix = pad_matrix(matrices[i], target_shape, 'right')
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


def smart_crop(matrix_to_crop: np.array):
    first_line_with_positive_cell = find_first_positive_row(matrix_to_crop, MINIMUM_LIGHT_PIXELS_IN_LINE)
    first_line_with_positive_cell = min(first_line_with_positive_cell, SNAPSHOT_SIZE[1] - slice_size()) # Avoid out of bound problem

    matrix_to_crop = matrix_to_crop[
        first_line_with_positive_cell:
        first_line_with_positive_cell + slice_size()]
    return matrix_to_crop


def crop_prediction(prediction: np.ndarray):
    cropped_matrices = []

    all_images_paths = list_directory_contents(
    get_default_input_path(), allowed_extentsions=[".png", ".jpeg", ".jpg"])

    assert len(all_images_paths) == len(prediction), \
    f"There should be the same quantity of proccessed"\
      f"images {len(all_images_paths)} as crude ones {len(prediction)}"
    
    for image_path, prediction in zip(all_images_paths, prediction):
        try:
            cropped_matrix = np.copy(smart_crop(prediction))
            square_matrix = crop_to_square(cropped_matrix)
            cropped_matrices.append(square_matrix)
        except DamagedSnapshotException:
            logger.error(f"Image {image_path} was damaged, not enough light pixels")
            raise DamagedSnapshotException("Error: the given video is has too some problematic shots and, re-take the video")
    
    return cropped_matrices


def crop_to_square(rectangle_to_crop):
    x, y = rectangle_to_crop.shape
    if y < x:
        raise ValueError(f"Matrix width must be at least equal to its height, but got shape {rectangle_to_crop.shape}")

    crop_amount = (y - x) // 2

    square_result = rectangle_to_crop[:, crop_amount:crop_amount + x]
    
    return square_result

def in_memory_video_to_video_capture(uploaded_file):
    with NamedTemporaryFile(delete=True, suffix='.mp4') as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file.flush()

        video = cv2.VideoCapture(temp_file.name)

        if not video.isOpened():
            raise ValueError("Could not open video file.")
    return video

def get_video_fps(video: cv2.VideoCapture):
    return int(video.get(cv2.CAP_PROP_FPS))


def take_video_snapshots(video: cv2.VideoCapture, snapshot_interval:int, fps: int):
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    step_size = fps * snapshot_interval 
    snapshot_count = max(total_frames // step_size, 1)  + 1 # At least one snapshot
    print("VID total frames, ", total_frames, " step size ", step_size, "snapshot_count " , snapshot_count)

    snapshots = []
    for i in range(0, snapshot_count):
        print("frame taken " ,i * step_size)
        frame_number = i * step_size
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            snapshots.append(frame_pil)
        else:
            break
    print("VID result", len(snapshots))
    #IMPORTANT it is the user's responsibility to perform video.release() 
    return snapshots

def take_gyroscope_snapshots(gyroscope_data:list, snapshot_interval:int, fps:int):

    result = gyroscope_data[::(snapshot_interval * fps)]
    print("GYR total frames, ", len(gyroscope_data), " step size ", snapshot_interval * fps, "snapshot_count " , len(result))

    return result

def processing_cleanup(directory):
    if not os.path.exists(directory): 
        os.mkdir(directory)
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Removed file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Removed directory and its contents: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

def save_pictures(snapshots:list, input_dir:str):
    for idx, snapshot in enumerate(snapshots):
        snapshot.save(os.path.join(input_dir, f"{idx}.jpg")) 

def save_map(map: np.ndarray, map_name: str):
    map_image = Image.fromarray(map)
    map_image = map_image.convert("RGB")
    save_path = os.path.join(get_default_output_path(), map_name)
    map_image.save(save_path)


if __name__ == "__main__":
    
    input_path = "backend/algorithm/input/"
    all_images = list_directory_contents(input_path, [".jpg"])

    for path in all_images: 
        prefixed_path = prefix_from_absolute_path(path, "sqr_")
        crop_image_to_square(path,prefixed_path)