import cv2

from ..predicate_target_filter import predicate_target_filter
from ...ovl_math.shape_fill_ratios import rotating_rectangle_fill_ratio
from ...utils.types import RangedNumber


@predicate_target_filter
def rotated_rectangle_filter(contour, min_area_ratio: RangedNumber(0, 1) = 0.8):
    """
    Receives a list of contours and returns only those that are approximately a rectangle regardless
    of the angle of rotation.

    :param contour: contour currently being evaluated
    :param min_area_ratio: the minimum ratio between the contour area and the bounding shape
    :return: the contour list filtered.
    """
    fill_ratio, _, _ = rotating_rectangle_fill_ratio(contour)
    contour_perimeter = cv2.arcLength(contour, True)
    approximation = cv2.approxPolyDP(contour, 0.02 * contour_perimeter, True)
    return fill_ratio > min_area_ratio and len(approximation) == 4
