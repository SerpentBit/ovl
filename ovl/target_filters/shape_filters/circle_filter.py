from ...ovl_math.shape_fill_ratios import circle_fill_ratio
from ..predicate_target_filter import predicate_target_filter
from ...utils.types import RangedNumber


@predicate_target_filter
def circle_filter(contour, min_area_ratio: RangedNumber(0, 1) = 0.7):
    """
    Filters out contour which are not approximately circle.
    
    :param contour: list of contours (numpy arrays) to be filtered
    :param min_area_ratio: minimum ratio between the area of the enclosing
                         circle and the contour (contour /enclosing circle)
    :return: the list of contours that fit the criteria
    """

    fill_ratio, _ = circle_fill_ratio(contour)
    return fill_ratio >= min_area_ratio
