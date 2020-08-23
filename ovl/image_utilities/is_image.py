import numpy as np


def is_greyscale_image(image: np.ndarray) -> bool:
    """
    A function that checks if an image is a greyscale image (an image where pixels are a number - has 1 color channel)

    :param image: the image to be checked, a numpy array
    """
    return len(image.shape) == 2


is_image_grayscale = is_greyscale_image


def is_color_image(image: np.ndarray) -> bool:
    """
    A function that checks if an image is a color image (each pixel is not one value but multiple color components)

    :param image: the image to be checked, a numpy array
    """
    return len(image.shape) == 3
