# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
from numpy import ndarray
from . import Geometry
from sys import version_info


if version_info[0] == 3:
    xrange = range


def validate(contour, target_amount):
    if contour is None:
        return False
    elif contour is []:
        return False
    elif type(contour) is ndarray and target_amount > 1:
        return False
    elif type(contour) is list and len(contour) < target_amount:
        return False
    else:
        return True


def alert_directions(contour, target_amount, img_size=(320, 240)):
    """
    Action: returns true if targets were found false otherwise
    :param contour:
    :param target_amount:
    :param img_size:
    :return:
    """
    return 1 if validate(contour, target_amount) else 0


def xy_center_directions(contour, target_amount, img_size=(320, 240), invert=False):
    """
    Action: returns the directions for the robot for the given contours for the x and y axis
    :param contour: the final contours - your targets
    :param target_amount: the amount of targets wanted
    :param img_size: the size of the image (width, height)
    :param invert: if the value should be inverted (max - value)
    :return: the directions
    """
    width, height = img_size
    x_ratio = 2000 / width
    y_ratio = 2000 / height
    if not validate(contour, target_amount):
        return False
    if type(contour) is ndarray:
        contour = [contour]
    x_sum = 0
    y_sum = 0
    contour = contour[:target_amount]
    for currentContour in contour:
        x, y = Geometry.get_contour_center(currentContour)
        x_sum += x
        y_sum += y
    x_res = x_sum / len(contour)
    y_res = y_sum / len(contour)
    x_res *= x_ratio
    y_res *= y_ratio
    if invert:
        return str(2000 - x_res) + str(2000 - y_res)
    return str(x_res) + str(y_res)


def y_center_directions(contour, target_amount, img_size=(320, 240), invert=False):
    """
    Action: returns the directions for the robot for the given contours for the y axis only
    :param contour: the final contours - your targets
    :param target_amount: the amount of targets wanted
    :param img_size: the size of the image (width, height)
    :param invert: if the value should be inverted (max - value)
    :return: the directions
    """
    _, height = img_size
    y_ratio = 2000 / height
    if not validate(contour, target_amount):
        return False
    if type(contour) is ndarray:
        contour = [contour]
    y_sum = 0
    contour = contour[:target_amount]
    for currentContour in contour:
        x, y = Geometry.get_contour_center(currentContour)
        y_sum += y
    y_res = y_sum / len(contour)
    if invert:
        return 2000 - (y_res * y_ratio)
    return y_res * y_ratio


def x_center_directions(contour, target_amount, img_size=(320, 240), invert=False):
    """
    Action: returns the directions for the robot for the given contours for the x axis only
    :param contour: the final contours - your targets
    :param target_amount: the amount of targets wanted
    :param img_size: the size of the image (width, height)
    :param invert: if the value should be inverted (max - value)
    :return: the directions
    """
    width, _ = img_size
    x_ratio = 2000 / width
    if not validate(contour, target_amount):
        return False
    if type(contour) is ndarray:
        contour = [contour]
    x_sum = 0
    contour = contour[:target_amount]
    for currentContour in contour:
        x, y = Geometry.get_contour_center(currentContour)
        x_sum += x
    x_res = x_sum / len(contour)
    if invert:
        return 2000 - (x_res * x_ratio)
    return x_res * x_ratio

