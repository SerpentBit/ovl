import cv2

from ..contour_filter import target_filter
from ...math.shape_fill_ratios import rectangle_fill_ratio_straight
from ...utils.types import RangedNumber


@target_filter
def vertical_rectangle_filter(contour_list, min_area_ratio: RangedNumber(0, 1) = 0.7):
    """
    Receives a list of contours and returns only the ones that are approximately a vertical rectangle
    :param contour_list: List of Contours to filter
    :type contour_list: List
    :param min_area_ratio: minimum ratio between the area of the contours and the bounding shape
    :return: the contour list filtered.
    """
    ratio_list = []
    output_list = []
    for current_contour in contour_list:
        fill_ratio, contour_width, contour_height = rectangle_fill_ratio_straight(current_contour)
        peri = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and contour_width < contour_height and len(approximation) == 4:
            output_list.append(current_contour)
            ratio_list.append(fill_ratio)
    return output_list, ratio_list
