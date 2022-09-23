import numpy as np

import math


def y_intersection(line_slope, intercept, x_value):
    """
    Finds the y value of the line (y = mx + b) at point x and returns the point
    This basically solves y = mx + b

    :param line_slope: slope of the line (m)
    :param intercept: the intercept of the line (b)
    :param x_value: the value to be used (substituted with x)
    :return: the y value
    """
    return x_value, line_slope * x_value + intercept


def x_intersection(line_slope, intercept, y_value):
    """
    Calculates the x value of which the line according to the given y value
    This basically solves y = mx + b

    :param line_slope: slope of the line (m)
    :param intercept: the intercept of the line (b)
    :param y_value: the value to be used (substituted with x)
    :return: the y value
    """
    return (y_value - intercept) / float(line_slope), y_value if line_slope != 0 else (0, y_value)


def slope(first_point, second_point):
    """
    Returns the slope between 2 points

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
    Calculates the area of a circle with the given radius.

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
    return math.sqrt((first_point[0] - second_point[0]) ** 2 + (first_point[1] - second_point[1]) ** 2)


def regular_polygon_angle(side_amount: int) -> float:
    """
    Returns the inner angle of a polygon with the given amount of sides

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


def law_of_cosine(first_point, second_point, third_point) -> float:
    """
    Finds the angle BAC  in degrees given that first_point = A second point = B and third point = C
    """
    first_length = distance_between_points(first_point, second_point)
    second_length = distance_between_points(first_point, third_point)
    third_length = distance_between_points(second_point, third_point)
    angle = (first_length ** 2 + second_length ** 2 - third_length ** 2) / (first_length * second_length * 2)
    return math.degrees(angle)
