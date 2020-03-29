import typing
from functools import reduce
from typing import Tuple

import cv2
import numpy as np

from ovl import distance_between_points, law_of_cosine


def target_size(contours: typing.List[np.ndarray]) -> float:
    """
    Returns the sum of contour areas
    """
    return sum(map(cv2.contourArea, contours))


def open_arc_length(contour: np.ndarray) -> float:
    """
     Returns the arc length of an "open" contour
    :param contour:
    :return:
    """
    return cv2.arcLength(contour, False)


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
