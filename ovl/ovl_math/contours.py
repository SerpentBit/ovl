import typing
from functools import reduce
from typing import Tuple

import cv2
import numpy as np

from ovl.ovl_math.geometry import distance_between_points, law_of_cosine
from ovl.ovl_math.shape_fill_ratios import circle_fill_ratio
from ovl.image_filters.image_filters import crop_image

__all__ = [
    "target_size", "open_arc_length", "open_contour_approximation",
    "contour_center", "contour_average_center", "contour_approximation",
    "contour_lengths_and_angles", "calculate_normalized_screen_space",
    "circle_rating", "crop_contour_region", "contour_average_color"]


def target_size(contours: typing.List[np.ndarray]) -> float:
    """
    Returns the sum of contour areas of a list of contours
    """
    return sum(list(map(cv2.contourArea, contours)))


def open_arc_length(contour: np.ndarray) -> float:
    """
    Returns the arc length of an "open" contour
    """
    return cv2.arcLength(contour, False)


def open_contour_approximation(contour: np.ndarray, approximation_coefficient: float = 0.02):
    """
    Returns the vertices of the approximation of the contour
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
                         'try using area_filter to remove small contours,'
                         ' try adding an area_filter or increasing an existing one')
    return center_x, center_y


def _contour_center_sum(point_sum, contour):
    """
    Helper function for contour_average_center
    """

    def cumulate_points(first_point, second_point):
        return first_point[0] + second_point[0], first_point[1] + second_point[1]

    current_contour_center = contour_center(contour)
    return cumulate_points(point_sum, current_contour_center)


def contour_average_center(contours) -> Tuple[float, float]:
    """
    Calculates the average center of a list of contours

    :param contours: the list of contours
    :return: the polygon_filter_average center  (x,y)
    """
    contour_amount = float(len(contours))
    point_sum = reduce(_contour_center_sum, contours, (0, 0))
    average = (point_sum[0] / contour_amount, point_sum[1] / contour_amount)
    return average


def contour_approximation(contour, approximation_coefficient=0.02):
    """
    Returns the approximation of the contour

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
        vertex_index = index + 1 if index != len(approximation) - 1 else 0
        current_length = distance_between_points(point, vertices[vertex_index])
        current_angle = law_of_cosine(vertices[index - 1], point, vertices[vertex_index])
        lengths.append(current_length)
        angles.append(current_angle)

    return vertices, lengths, angles


def calculate_normalized_screen_space(contours: typing.Union[typing.List[np.ndarray], np.ndarray], image):
    """
    This function Calculates the center of the contours and converts it to normalized screen space,
    Which is the x and y values in relation to the center of the image

    This allows normalized values regardless of image size!



    :param contours: One Contour or a list of contours which their center should be calculated
    :param image: the image from which it was found
    :return: x, y in normalized screen space
    """
    height, width, _ = image.shape
    x, y = contour_average_center(contours)
    x /= width / 2
    y /= height / 2
    return x - 1, y - 1


def circle_rating(contour, area_factor=0.9, radius_factor=0.8):
    """
    Returns a rating of how close is the circle to being a circle

    :param contour: the contour that its rating is calculated
    :param area_factor: the factor (p-value) that separates an area ratio that is a circle and one that isn't
    :param radius_factor: the factor (p-value) that separates a radius ratio that is a circle and one that isn't
    :return: the circle rating for the given contour
    """
    fill_ratio, radius = circle_fill_ratio(contour)
    _, _, width, height = cv2.boundingRect(contour)
    radius_ratio = ((((radius * 2) ** 2) / (float(width) * height)) ** 0.5)
    rating = (radius_ratio * radius_factor) * (fill_ratio * area_factor)
    return rating


def crop_contour_region(contour: np.ndarray, image: np.ndarray):
    """
    Returns a region of the image where the contour (using its bounding box)

    :param contour: the object found in the image, a numpy array
    :param image: the image from which the contour was found
    :return: the image  region that contains the contour
    """
    corner_x, corner_y, width, height = cv2.boundingRect(contour)
    return crop_image(image, (corner_x, corner_y), (width, height))


def contour_average_color(contours: typing.List[np.ndarray], image: np.ndarray):
    """
    Calculates the polygon_filter_average color (in hsv) of all the pixels of a list of contours in the image.

    :param contours: a list of contour(s) detected in the image
    :param image: the image where the contours where detected, numpy array
    :return: hsv color (h, s, v) tuple of the average color
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    mask = np.zeros(image.shape, np.uint8)
    if isinstance(contours, np.ndarray):
        contours = [contours]
    cv2.drawContours(mask, contours, -1, 255, -1)
    return cv2.mean(hsv, mask)
