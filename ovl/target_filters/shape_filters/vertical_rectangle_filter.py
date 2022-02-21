import cv2

from ..predicate_target_filter import predicate_target_filter
from ...ovl_math.shape_fill_ratios import rectangle_fill_ratio_straight
from ...utils.types import RangedNumber


@predicate_target_filter
def vertical_rectangle_filter(contour, min_area_ratio: RangedNumber(0, 1) = 0.7):
    """
    Receives a list of contours and returns only the ones that are approximately a vertical rectangle

    :param contour: contour to be evaluated
    :param min_area_ratio: minimum ratio between the area of the contours and the bounding shape
    :return: the contour list filtered.
    """
   
    fill_ratio, contour_width, contour_height = rectangle_fill_ratio_straight(contour)
    perimeter = cv2.arcLength(contour, True)
    approximation = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    return fill_ratio > min_area_ratio and contour_width < contour_height and len(approximation) == 4
