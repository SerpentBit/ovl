import cv2

from ..predicate_target_filter import predicate_target_filter
from ...ovl_math.shape_fill_ratios import circle_fill_ratio
from ...utils.types import RangedNumber


@predicate_target_filter
def constraining_circle_filter(contour, min_area_ratio: RangedNumber(0, 1) = 0.80,
                               min_len_ratio: RangedNumber(0, 1) = 0.9):
    """
    Filters out contour which are not approximately circle, also limits by radius ratio (unlike circle_filter).

    :param contour: a contour (numpy.ndarray) to be filtered
    :param min_area_ratio: minimum ratio between the area of the enclosing
    circle and the contour (contour /enclosing circle)
    :param min_len_ratio: minimum ratio between the radius of the enclosing circle and the enclosing rectangle.
    :return: the list of contours that fit the criteria
    """
    fill_ratio, radius = circle_fill_ratio(contour)
    _, _, rectangle_width, rectangle_height = cv2.boundingRect(contour)
    radius_ratio = ((2 * radius) ** 2) / float(rectangle_width) * rectangle_height
    return min_len_ratio <= (radius_ratio ** 0.5) and min_area_ratio <= fill_ratio
