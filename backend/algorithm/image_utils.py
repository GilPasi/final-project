import numpy as np
import logging
import cv2

from PIL import Image
from utils import list_directory_contents, prefix_from_absolute_path
from damaged_snapshot_exception import DamagedSnapshotException
from utils import get_default_input_path, slice_size,\
MINIMUM_LIGHT_PIXELS_IN_LINE, SNAPSHOT_SIZE


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

def glue_map(matrices, orientations):
    if len(matrices) != len(orientations):
        raise ValueError("The number of matrices and orientations must be the same.")
    
    result = matrices[0]
    for i in range(1, len(matrices)):
        if orientations[i] == 'horizontal':
            result = np.hstack((matrices[i], result))
        elif orientations[i] == 'vertical':
            result = np.vstack((matrices[i], result))
        else:
            raise ValueError("Invalid orientation. Use 'horizontal' or 'vertical'.")
    
    return result

def smart_crop(matrix_to_crop: np.array):
    first_line_with_positive_cell = find_first_positive_row(matrix_to_crop, MINIMUM_LIGHT_PIXELS_IN_LINE)
    first_line_with_positive_cell = min(first_line_with_positive_cell, SNAPSHOT_SIZE[1] - slice_size())

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
            cropped_matrices.append(cropped_matrix)
        except DamagedSnapshotException:
            logging.basicConfig(filename='image_processing.log', 
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error(f"Image {image_path} was damaged, not enough light pixels")
    
    return cropped_matrices

 # TODO: test this 
def extract_snapshots(self, video, interval_seconds:int = 0 ):
    video_data = video.read()
    np_arr = np.frombuffer(video_data, np.uint8)
    cap = cv2.VideoCapture(cv2.imdecode(np_arr, cv2.IMREAD_COLOR))

    if not cap.isOpened():
        print("Error opening video stream or file")

    frame_number = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps * interval_seconds)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number % interval == 0 or saved_frame_count == 0:
            frame_path = f"frame_{saved_frame_count}.jpg"
            cv2.imwrite(frame_path, frame)
            print(f"Saved {frame_path}")
            saved_frame_count += 1

        frame_number += 1
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    
    input_path = "backend/algorithm/input/"
    all_images = list_directory_contents(input_path, [".jpg"])

    for path in all_images: 
        prefixed_path = prefix_from_absolute_path(path, "sqr_")
        crop_image_to_square(path,prefixed_path)