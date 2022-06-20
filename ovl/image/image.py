from functools import lru_cache
from typing import Union, Tuple

import cv2
import numpy as np

from .constants import IMAGE_BLUR_CACHE_SIZE
from .open_image import open_image
from ..ovl_math.image import distance_from_frame, distance_between_points, image_center
from ..utils.types import Point


# TODO: Add http fetching support
# TODO: Docstring
def source_to_image(source):
    """
    Converts a source to an image.
    :param source: The source to convert.
    :return: The image.
    """
    if isinstance(source, str):
        return open_image(source)
    elif isinstance(source, np.ndarray):
        return source
    else:
        raise ValueError(f"Invalid source type {source}.")


# TODO: Create Image class that can be used to manipulate images.
# TODO: Docstring


class Image:
    def __init__(self, image):
        self.image = image

    # region Image Properties

    @property
    def size(self):
        return self.image.shape[0] * self.image.shape[1]

    @property
    def width(self):
        return self.image.shape[0]

    @property
    def height(self):
        return self.image.shape[1]

    @property
    def channels(self):
        return self.image.shape[2]

    @property
    def dimensions(self):
        return self.image.shape[:2]

    @property
    def shape(self):
        return self.image.shape

    def __getitem__(self, key):
        return self.image[key]

    def __setitem__(self, key, value):
        self.image[key] = value

    # endregion

    # region Generic Image Operations
    def __repr__(self):
        return self.image.__repr__()

    def __str__(self):
        return self.image.__str__()

    def __iter__(self):
        return self.image.__iter__()

    # endregion

    # region Functionalities with other images
    def __add__(self, other):
        if isinstance(other, Image):
            return Image(self.image + other.image)
        elif isinstance(other, np.ndarray):
            return Image(self.image + other)
        else:
            raise TypeError("Can only add images or numpy arrays to images")

    def __sub__(self, other):
        if isinstance(other, Image):
            return Image(self.image - other.image)
        elif isinstance(other, np.ndarray):
            return Image(self.image - other)
        else:
            raise TypeError("Can only subtract images or numpy arrays from images")

    # endregion

    # region Points
    @property
    def image_center(self):
        return image_center(self.dimensions)

    def distance_from_frame(self, point: Point):
        return distance_from_frame(point, self.dimensions)

    @lru_cache(maxsize=None)
    def distance_from_center(self, point: Point):
        return distance_between_points(point, self.image_center)

    # endregion

    # region Blurs
    @lru_cache(maxsize=IMAGE_BLUR_CACHE_SIZE)
    def gaussian_blur(self, kernel: Union[int, Tuple] = 5, sigma_x: float = 0, sigma_y: float = None,
                      border_type: int = None):
        """
        Blurs the image with a gaussian kernel.
        The result is cached for faster performance.

        :param kernel: The size of the kernel, must be an odd number larger than 1 (3, 5, 7).
         If a tuple is given, it is used as the kernel size.
        :param sigma_x: The standard deviation of the gaussian in the x direction.
        :param sigma_y: The standard deviation of the gaussian in the y direction. If None, it is set to sigma_x.
        :param border_type: The border type. See cv2.blur for more information.
        :return: The blurred image.
        """
        if isinstance(kernel, int):
            kernel = (kernel, kernel)
        return Image(cv2.GaussianBlur(self.image, kernel, sigma_x, sigma_y, border_type))

    @lru_cache(maxsize=IMAGE_BLUR_CACHE_SIZE)
    def median_blur(self, kernel_size: int = 3):
        return Image(cv2.medianBlur(self.image, kernel_size))

    @lru_cache(maxsize=IMAGE_BLUR_CACHE_SIZE)
    def bilateral_blur(self, kernel_size: int = 5, sigma_color: float = 75, sigma_space: float = 75):
        return Image(cv2.bilateralFilter(self.image, kernel_size, sigma_color, sigma_space))

    @lru_cache(maxsize=IMAGE_BLUR_CACHE_SIZE)
    def rotate(self, angle: float):
        """
        Rotates the image by the given angle.
        The result is cached for faster performance.

        :param angle: The angle in degrees.
        :return: The rotated image.
        """
        return Image(cv2.rotate(self.image, angle))
    # endregion
