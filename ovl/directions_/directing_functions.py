from numpy import ndarray

import ovl.math_.contours
from ..math_ import geometry


def xy_center_directions(contours, image: ndarray):
    """
    Returns the director for the robot for the given contours for the x and y axis
    :param contours: the final contours found after filtering - your targets
    :param image: the image from which it was found
    :return: the normalized screen space x and y coordinates of your final targets
    """
    height, width, _ = image.shape
    x, y = ovl.math_.contours.contour_average_center(contours)
    x /= width / 2
    y /= height / 2
    return x - 1, y - 1


def y_center_directions(contours, image: ndarray):
    """
    Returns the director for the robot for the given contours for the y axis only
    the value of the direction is between -1 and 1
    :param contours: the final contours - your targets
    :param image: the image from which it was found
    :return: the normalized screen space y coordinate of your final targets
    """
    height, _, _ = image.shape
    _, y = ovl.math_.contours.contour_average_center(contours)
    y /= height / 2
    return y - 1


def x_center_directions(contours, image: ndarray):
    """
    Returns the director for the robot for the given contours for the x axis only
    :param contours: the final contours - your targets
    :param image: the image from which it was found
    :return: the normalized screen space x coordinate of your final targets
    """
    _, width, _ = image.shape
    x, _ = ovl.math_.contours.contour_average_center(contours)
    x /= width / 2
    return x - 1


def center_directions(contours, image: ndarray):
    """
    Returns the average center of the contours
    or list of contours that are the final targets

    This is the default directions function since it
    doesnt calculate any directions, only finds the center
    :param contours: the final contours - your targets
    :param image: the image from which it was found
    """
    return ovl.math_.contours.contour_average_center(contours)


def target_amount_directions(contours, image: ndarray):
    """
    Counts the amount of successful object detections.
    :param contours: the final contours - your targets
    :param image: the image from which it was found
    :return: the amount of targets detected
    """
    return len(contours)

