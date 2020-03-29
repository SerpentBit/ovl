# Copyright 2018 - 2019 Ori Ben-Moshe - All rights reserved.

import cv2
import numpy as np
import typing
import math
from typing import Union

from ovl import contour_center
from ovl.math_.shape_fill_ratios import circle_fill_ratio


def y_intersection(line_slope, intercept, x_val):
    """
     finds the y value of the line (y = mx + b) at point x and returns the point
    :param line_slope: slope of the line (m)
    :param intercept: the intercept of the line (b)
    :param x_val: the value to be used (substituted with x)
    :return: the y value
    """
    return x_val, line_slope * x_val + intercept


def x_intersection(line_slope, intercept, y_val):
    """
     calculates the x value of which the line according to the given y value
    :param line_slope:
    :param intercept:
    :param y_val:
    :return:
    """
    return (y_val - intercept) / float(line_slope), y_val if line_slope != 0 else (0, y_val)


def horizon_angle(point: Union[np.ndarray, typing.Tuple[int, int]], field_of_view: float, image_width: int) -> float:
    """
     returns the angle compared to the center of the image for a given field of view image width and point
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
     returns the angle compared to the center of the image for a given field of view image height and point
    :param point: the x val or center
    :param field_of_view: the vertical field of view
    :param image_height: the image height
    :return: the angle compared to the center of the image , negative up positive down6.
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


def slope(first_point, second_point):
    """
     returns the slope between 2 points
    :param first_point: first point (x,y)
    :param second_point: second point (x,y)
    :return: the slope
    """
    return 0. if first_point[0] == second_point[0] else\
        ((float(first_point[1]) - float(second_point[1])) / (float(first_point[0]) - float(second_point[0])))


def angle_between_points(first_point, second_point):
    """
    Calculates the angle between the 2 points and the horizontal axis
    :param first_point: the first point (2d)
    :param second_point: the second point  (2d)
    :return: the angle
    """
    return math.degrees(math.atan(slope(first_point, second_point)))


def contour_angle_line(contour):
    """
    Returns the angle of the line created by the top-most and
    bottom-most points of a contour
    :param contour: the contour, a numpy array
    :return: the angle in degrees
    """
    if type(contour) != np.ndarray:
        raise TypeError("Contour must be a numpy array")
    topmost = tuple(contour[contour[:, :, 1].argmin()][0])
    bottommost = tuple(contour[contour[:, :, 1].argmax()][0])
    return angle_between_points(topmost, bottommost)


def circle_area(radius):
    """
     calculates the area of a circle with the given radius.
    :param radius: The radius of the circle
    :return: Area of the circle
    """
    return math.pi * (radius ** 2)


def distance_between_points(first_point, second_point):
    """
     Calculates the Distance between 2 points. (x^2 + y^2) ^ 0.5
    :param first_point: tuple of x and y value of point 1
    :param second_point: tuple of x and y value of point 2
    :return: Float value of the distance between the 2 points
    :rtype: float
    """
    return ((first_point[0] - second_point[0]) ** 2 + (first_point[1] - second_point[1]) ** 2) ** 0.5


def regular_polygon_angle(side_amount: int) -> float:
    """
     returns the inner angle of a polygon with the given amount of sides
    :param side_amount: amount of sides the polygon has
    :return:
    """
    return (side_amount - 2) * (180 / side_amount)


def polygon_area(side_length, amount_of_sides):
    """
     area of a polygon of
    :param side_length: side_length of a side of the polygon
    :param amount_of_sides: Amount of sides the polygon has
    :return: the area of the polygon
    """
    angle = 180 / amount_of_sides
    return 0.25 * amount_of_sides * (side_length ** 2) * (math.cos(math.radians(angle)) / math.sin(math.radians(angle)))


def circle_rating(contour, area_factor=0.9, radius_factor=0.8):
    """
     returns a rating of how close is the circle to being a circle
    :param contour: the contour that its rating is calculated
    :param area_factor: the factor (p-value) that separates an area ratio that is a circle and one that isn't
    :param radius_factor: the factor (p-value) that separates an radius ratio that is a circle and one that isn't
    :return:
    """
    fill_ratio, radius = circle_fill_ratio(contour)
    _, _, width, height = cv2.boundingRect(contour)
    radius_ratio = ((((radius * 2) ** 2) / float(width) * height) ** 0.5)
    rating = (radius_ratio * radius_factor) * (fill_ratio * area_factor)
    return rating


def law_of_cosine(first_point, second_point, third_point) -> float:
    """
    Finds the angle BAC  in degrees given that first_point = A second point = B and third point = C
    """
    first_length = distance_between_points(first_point, second_point)
    second_length = distance_between_points(first_point, third_point)
    third_length = distance_between_points(second_point, third_point)
    angle = (first_length ** 2 + second_length ** 2 - third_length ** 2) / (first_length * second_length * 2)
    return math.degrees(angle)


