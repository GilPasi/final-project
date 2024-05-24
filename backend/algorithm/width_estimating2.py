import numpy as np

def calculate_fov(sensor_width, focal_length):
    return 2 * np.arctan(sensor_width / (2 * focal_length))

def find_trail_indices(image):
    return np.where(image > 0)

def calculate_average_depth(image, trail_indices):
    depths = image[trail_indices]
    return np.mean(depths)

def calculate_scale_factor(fov, avg_depth, trail_width_pixels):
    width_at_avg_depth = 2 * avg_depth * np.tan(fov / 2)
    return width_at_avg_depth / trail_width_pixels

def resize_image(image, scale_factor):
    new_width = int(image.shape[1] * scale_factor)
    normalized_image = np.zeros((image.shape[0], new_width))
    for i in range(image.shape[0]):
        normalized_image[i] = np.interp(
            np.linspace(0, image.shape[1] - 1, new_width),
            np.arange(image.shape[1]),
            image[i]
        )
    return normalized_image

def normalize_trail_width(image, focal_length, sensor_width):
    fov = calculate_fov(sensor_width, focal_length)

    trail_indices = find_trail_indices(image)
    if trail_indices[1].size == 0:
        return image 
    
    avg_depth = calculate_average_depth(image, trail_indices)
    c = np.max(trail_indices[1])
    d = np.min(trail_indices[1])
    trail_width_pixels = np.max(trail_indices[1]) - np.min(trail_indices[1]) + 1
    scale_factor = calculate_scale_factor(fov, avg_depth, trail_width_pixels)
    
    return resize_image(image, scale_factor)
