import cv2

from ..predicate_target_filter import predicate_target_filter
from ...ovl_math.shape_fill_ratios import rectangle_fill_ratio_straight
from ...utils.types import RangedNumber


@predicate_target_filter
def horizontal_rectangle_filter(contour, min_area_ratio: RangedNumber(0, 1) = 0.8):
    """
    Receives a contour and return True only those that are approximately a horizontal rectangle

    :param contour: contour (numpy.ndarray) to be filtered
    :param min_area_ratio
    :return: the contour list filtered.
    """
    fill_ratio, contour_width, contour_height = rectangle_fill_ratio_straight(contour)
    perimeter = cv2.arcLength(contour, True)
    approximation = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    return fill_ratio > min_area_ratio and contour_width > contour_height and len(approximation) == 4
