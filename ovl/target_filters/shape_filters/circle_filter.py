from ovl.ovl_math.shape_fill_ratios import circle_fill_ratio
from ovl.target_filters.predicate_target_filter import predicate_target_filter
from ovl.utils.types import RangedNumber


@predicate_target_filter
def circle_filter(contour_list, min_area_ratio: RangedNumber(0, 1) = 0.7):
    """
    Filters out contour which are not approximately circle.
    
    :param contour_list: list of contours (numpy arrays) to be filtered
    :param min_area_ratio: minimum ratio between the area of the enclosing
                         circle and the contour (contour /enclosing circle)
    :return: the list of contours that fit the criteria
    """
    output = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio, radius = circle_fill_ratio(current_contour)
        if min_area_ratio <= fill_ratio:
            output.append(current_contour)
            ratio_list.append(fill_ratio)
    return output, ratio_list
