# Copyright 2018 - 2019 Ori Ben-Moshe - All rights reserved.
from functools import reduce

import cv2
import numpy as np
import typing
import math
from typing import List, Tuple, Union

from .default_math_functions import math_funcs


def target_size(contours: typing.List[np.ndarray]) -> float:
    """
    Returns the sum of contour areas
    """
    return sum(map(cv2.contourArea, contours))


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


def distance_from_frame(point, image_dimensions):
    """
    Action calculates the distance of a given point from the frame of the image based on the vector from the center
    and the point
    :param point: point (x,y tuple) or contour (numpy array)
    :param image_dimensions: the size of the image, (width, height)
    :return: the distance
    """
    point = contour_center(point) if type(point) is np.ndarray else point
    image_center = (image_dimensions[0] / 2 - .5, image_dimensions[1] / 2 - .5)
    line_slope = slope(point, image_center)
    intercept = - line_slope * point[0] + point[1]
    xs = (image_dimensions[0] - 1, 0)
    ys = (image_dimensions[1] - 1, 0)
    y_distances = [distance_between_points(y_intersection(line_slope, intercept, y), point) for y in ys]
    x_distances = [distance_between_points(x_intersection(slope, intercept, x), point) for x in xs]
    return min(y_distances + x_distances)


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


def open_arc_length(contour: np.ndarray) -> float:
    """
     Returns the arc length of an "open" contour
    :param contour:
    :return:
    """
    return cv2.arcLength(contour, False)


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
     calculates the angle between the 2 points and the horizontal axis
    :param first_point: the first point (2d)
    :param second_point: the second point  (2d)
    :return: the angle
    """
    return math.degrees(math.atan(slope(first_point, second_point)))


def line_angle(contour):
    """
     returns the angle of the line created by the top-most and
    bottom-most points of a contour
    :param contour: the contour, a numpy array
    :return: the angle in degrees
    """
    if type(contour) != np.ndarray:
        raise TypeError("Contour must be a numpy array")
    topmost = tuple(contour[contour[:, :, 1].argmin()][0])
    bottommost = tuple(contour[contour[:, :, 1].argmax()][0])
    return angle_between_points(topmost, bottommost)


def open_contour_approximation(contour: np.ndarray, approximation_coefficient: float = 0.02):
    """
     returns the vertices of the approximation of the contour
    NOTE: for "open" (unclosed shape) contours only!
    :param contour: open contour (numpy array)
    :param approximation_coefficient: approximation coefficient
    :return: list of vertices
    """
    arc = approximation_coefficient * cv2.arcLength(contour, False)
    return cv2.approxPolyDP(contour, arc, False)


def calculate_math_expression(equation, value, additional_functions=None, symbol='x'):
    """
     calculates the result of a math expression with a variable
    :param equation: the equation with a variable to be calculated
    :param value: the value to be placed instead of the variable
    :param additional_functions: additional functions to be used
    :param symbol: The symbol in the equation representing the variable
    :return: the result of the variable
    """
    expression = equation.replace(symbol, str(value))
    if additional_functions is None:
        additional_functions = math_funcs

    exec('equation_res = ' + expression, additional_functions)
    return locals()['equation_res']


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


def rectangle_fill_ratio_straight(contour, reverse_div=False):
    """
     Returns the ratio between the contour and the straight bounding rectangle.
    :param contour: The contour to be compared
    :param reverse_div: If the rectangle's area should be divided by the contour.
    :return:  the ratio, the width of the bounding rectangle, the height of the bounding rectangle
    :rtype: float
    """
    _, _, width, height = cv2.boundingRect(contour)
    bounding_rectanlge_area = width * height
    contour_area = cv2.contourArea(contour)
    if reverse_div:
        return float(bounding_rectanlge_area) / contour_area, width, height
    return float(contour_area) / bounding_rectanlge_area, width, height


def triangle_fill_ratio(contour, triangle=None) -> float:
    """
    :param contour: numpy array
    :param triangle: convex hull for the minEnclosingTriangle function, can be ignored
    :return: returns the ratio between the contour and the bounding triangle
    :rtype: float
    """
    bounding_triangle_area, triangle = cv2.minEnclosingTriangle(contour, triangle)
    contour_area = cv2.contourArea(contour)
    return contour_area / float(bounding_triangle_area)


def rotating_rectangle_fill_ratio(contour: np.ndarray) -> typing.Tuple[float, float, float]:
    """
     Returns the ratio between the contour and the smallest bounding rectangle.
    :param contour: The contour to be compared
    :return: the ratio, the width of the bounding rectangle, the height of the bounding rectangle
    :rtype: float, float, float
    """
    rotated = cv2.minAreaRect(contour)
    bounding_rectangle_area = rotated[1][0] * rotated[1][1]
    contour_area = cv2.contourArea(contour)
    return float(contour_area) / bounding_rectangle_area, rotated[1][0], rotated[1][1]


def circle_fill_ratio(contour: np.ndarray) -> typing.Tuple[float, float]:
    """
     Returns the ratio between the contour and the smallest enclosing circle.
    :param contour: The contour to be compared
    :return: the ratio, the radius of the enclosing circle
    :rtype: float
    """
    _, enclosing_radius = cv2.minEnclosingCircle(contour)
    enclosing_circle_area = circle_area(enclosing_radius)
    contour_area = cv2.contourArea(contour)
    return float(contour_area) / enclosing_circle_area, enclosing_radius


def contour_center(contour: np.ndarray) -> Tuple[float, float]:
    """
     Returns the coordinates center of a contour
    :param contour: a single contour
    :return: X coordinate of center, Y coordinate of center
    """
    moments = cv2.moments(contour)
    try:
        area = float(moments['m00'])
        center_x, center_y = moments['m10'] / area, moments['m01'] / area
    except ZeroDivisionError:
        raise ValueError('Contour given is too small!,'
                         'try using area_filter to remove small contours (try min_area=20)')
    return center_x, center_y


def _contour_center_sum(point_sum, contour):
    """
    Helper function for contour_average_center
    """
    def _average_point_reduce(first_point, second_point):
        return first_point[0] + second_point[0], first_point[1] + second_point[1]
    current_contour_center = contour_center(contour)
    return _average_point_reduce(point_sum, current_contour_center)


def contour_average_center(contours) -> Tuple[float, float]:
    """
    Calculates the average center of a list of contours
    :param contours: the list of contours
    :return: the average center  (x,y)
    """
    return reduce(_contour_center_sum, contours, (0, 0))


def regular_polygon_angle(side_amount: int) -> float:
    """
     returns the inner angle of a polygon with the given amount of sides
    :param side_amount: amount of sides the polygon has
    :return:
    """
    return (side_amount - 2) * (180 / side_amount)


def contour_approximation(contour, approximation_coefficient=0.02):
    """
     returns the approximation of the contour
    :param contour: a numpy array
    :param approximation_coefficient: the coefficient of the contour length approximation
    :return:
    """
    perimeter = cv2.arcLength(contour, True)
    approximation = cv2.approxPolyDP(contour, approximation_coefficient * perimeter, True)
    return approximation


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


def contour_lengths_and_angles(contour, approximation_coefficient=0.02):
    """
    Returns a list of lengths and angles of a given contour.
    :param contour: contour (numpy array) to find its
    :param approximation_coefficient:
    :return: returns the list of sides
    """
    approximation = contour_approximation(contour, approximation_coefficient)
    vertices = []
    lengths = []
    angles = []
    for points in approximation:
        vertex = points[0][1], points[0][0]
        vertices.append(vertex)

    for index, point in enumerate(vertices):
        if index != len(approximation) - 1:
            current_length = distance_between_points(point, vertices[index + 1])
            current_angle = law_of_cosine(vertices[index - 1], point, vertices[index + 1])
        else:
            current_length = distance_between_points(point, vertices[0])
            current_angle = law_of_cosine(vertices[index - 1], point, vertices[0])
        lengths.append(current_length)
        angles.append(current_angle)

    return vertices, lengths, angles
