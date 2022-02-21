import cv2

from ..predicate_target_filter import predicate_target_filter
from ...ovl_math.shape_fill_ratios import triangle_fill_ratio
from ...utils.types import RangedNumber


@predicate_target_filter
def triangle_filter(contour, min_area_ratio: RangedNumber(0, 1) = 0.8,
                    approximation_coefficient: RangedNumber(0, 1) = 0.02):
    """
    Receives a list of contours and returns only those that are approximately
    triangle and have 3 sides.

    :param approximation_coefficient: the approximation coefficient affects
    how the contour's perimeter is approximated, the larger the number is (out of 1) the more the approximation of
    the contour is a line
    :param contour: contour to be evaluated
    :param min_area_ratio: the minimum ratio between the area of the contour and the bounding triangle
    :return: the filtered list
    """
  
    fill_ratio = triangle_fill_ratio(contour)
    peri = cv2.arcLength(contour, True)
    approximation = cv2.approxPolyDP(contour, approximation_coefficient * peri, True)
    return fill_ratio > min_area_ratio and len(approximation) == 3
  