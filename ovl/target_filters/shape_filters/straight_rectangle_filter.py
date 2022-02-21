import cv2

from ..predicate_target_filter import predicate_target_filter
from ...ovl_math.shape_fill_ratios import rectangle_fill_ratio_straight
from ...utils.types import RangedNumber


@predicate_target_filter
def straight_rectangle_filter(contour, min_area_ratio: RangedNumber(0, 1) = 0.8):
    """
    Receives a list of contours and returns only those that are approximately a rectangle that
    its sides are parallel to the frame of the image

    :param contour: List of Contours to filter
    :param min_area_ratio: The minimum ratio between the rectangle and the contour
    :type min_area_ratio: float
    :return: the contour list filtered.
    """

    fill_ratio, _, _ = rectangle_fill_ratio_straight(contour)
    perimeter = cv2.arcLength(contour, True)
    approximation = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    return fill_ratio > min_area_ratio and len(approximation) == 4
