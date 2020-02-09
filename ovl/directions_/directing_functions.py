# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
from numpy import ndarray

from ..math_ import geometry


def xy_center_directions(contours, image: ndarray):
    """
    Returns the director for the robot for the given contours for the x and y axis
    :param contours: the final contours found after filtering - your targets
    :param image: the image from which it was found
    :return: the director
    """
    height, width, _ = image.shape
    x, y = geometry.contour_average_center(contours)
    x /= width / 2
    y /= height / 2
    return x - 1, y - 1


def y_center_directions(contour, image: ndarray):
    """
    Returns the director for the robot for the given contours for the y axis only
    the value of the direction is between -1 and 1
    :param contour: the final contours - your targets
    :param image: the image from which it was found
    :return: the direction to move in the y axis (-1 to 1)
    """
    height, _, _ = image.shape
    _, y = geometry.contour_average_center(contour)
    y /= height / 2
    return y - 1


def x_center_directions(contour, image: ndarray):
    """
    Returns the director for the robot for the given contours for the x axis only
    :param contour: the final contours - your targets
    :param image: the image from which it was found
    :return: the direction to move in the y axis (-1 to 1)
    """
    _, width, _ = image.shape
    x, _ = geometry.contour_average_center(contour)
    x /= width / 2
    return x - 1


def center_directions(contour, image: ndarray):
    """
    Returns the average center of the contours
    or list of contours that are the final targets

    This is the default directions function since it
    doesnt calculate any directions, only finds the center
    :param contour: the final contours - your targets
    :param image: the image from which it was found
    """
    return geometry.contour_average_center(contour)
