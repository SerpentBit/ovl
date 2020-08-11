import math
import typing
from typing import Union

import numpy as np

from ovl import contour_center


def horizon_angle(point: Union[np.ndarray, typing.Tuple[int, int]], field_of_view: float, image_width: int) -> float:
    """
    Returns the angle compared to the center of the image for a given field of view image width and point

    :param point: the contour or its center
    :param field_of_view: the horizontal field of view
    :param image_width: the image width
    :return: the angle compared to the center of the image , negative left positive right.
    """
    point = point[0] if type(point) in (tuple, list, set) else point
    x_value = contour_center(point)[0] if type(point) is np.ndarray else point
    angle = math.atan((x_value - (image_width - 1) / 2) / float(focal_length(image_width, field_of_view)))
    return float(math.degrees(angle))


def vertical_angle(point: Union[np.ndarray, typing.Tuple[int, int]], field_of_view: float, image_height: int) -> float:
    """
    Returns the angle compared to the center of the image for a given field of view image height and point

    :param point: the x val or center
    :param field_of_view: the vertical field of view
    :param image_height: the image height
    :return: the angle compared to the center of the image , negative up positive down.
    """
    point = point[1] if type(point) in (tuple, list, set) else point
    y_val = contour_center(point)[1] if type(point) is np.ndarray else point
    angle = math.atan((y_val - (image_height - 1) / 2) / float(focal_length(image_height, field_of_view)))
    return float(math.degrees(angle))


def focal_length(image_width, field_of_view):
    """
    Calculates the focal length in pixels of the camera for a given an image width and field of view

    :param image_width: width of the image in pixels
    :param field_of_view:
    :return: calculates the focal length, a float
    """
    return image_width / float((2 * math.tan(math.radians(float(field_of_view / 2)))))
