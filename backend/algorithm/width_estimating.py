import math
import numpy as np 
def calculate_object_width(focal_length, sensor_width, distance, object_pixel_width, image_width):
    """
    Calculate the width of an object in a picture given the camera specs and object distance.

    :param focal_length: Focal length of the lens (mm)
    :param sensor_width: Sensor width (mm)
    :param distance: Distance to the object (meters)
    :param object_pixel_width: Width of the object in pixels
    :param image_width: Total width of the image in pixels
    :return: Width of the object in meters
    """
    # Focal length can be achieved using react native
    focal_length_m = focal_length / 1000
    
    sensor_width_m = sensor_width / 1000

    fov_rad = 2 * math.atan(sensor_width_m / (2 * focal_length_m))

    width_at_distance = 2 * distance * math.tan(fov_rad / 2)

    actual_width = (object_pixel_width / image_width) * width_at_distance

    return actual_width


def get_stripe_width(stripe: np.ndarray):
    start = end = 0
    for i in stripe: 
        if start == 0 and i > 0: 
            start = i
        elif start != 0 and i > 0:
            end = i
            return 
    return end - start
        
