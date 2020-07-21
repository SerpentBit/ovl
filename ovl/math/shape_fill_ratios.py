import typing

import cv2
import numpy as np

from .geometry import circle_area


def rectangle_fill_ratio_straight(contour, reverse_div=False):
    """
    Returns the ratio between the contour and the straight bounding rectangle.
    :param contour: The contour to be compared
    :param reverse_div: If the rectangle's area should be divided by the contour.
    :return:  the ratio, the width of the bounding rectangle, the height of the bounding rectangle
    :rtype: float
    """
    _, _, width, height = cv2.boundingRect(contour)
    bounding_rectangle_area = width * height
    contour_area = cv2.contourArea(contour)
    if reverse_div:
        return float(bounding_rectangle_area) / contour_area, width, height
    return float(contour_area) / bounding_rectangle_area, width, height


def triangle_fill_ratio(contour, triangle=None) -> float:
    """
    Returns the ratio between a given contour and the smallest enclosing rectangle
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
