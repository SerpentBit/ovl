import cv2

from ..contour_filter import contour_filter
from ...math_.geometry import rotating_rectangle_fill_ratio




@contour_filter
def rotated_rectangle_filter(contour_list, min_area_ratio=0.8):
    """
    Receives a list of contours and returns only those that are approximately a rectangle regardless
    of the angle of rotation.
    :param contour_list: List of Contours to filter
    :param min_area_ratio: the minimum ratio between the contour area and the bounding shape
    :return: the contour list filtered.
     """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio, w, h = rotating_rectangle_fill_ratio(current_contour)
        peri = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approximation) == 4:
            ratio_list.append(fill_ratio)
            output_list.append(current_contour)
    return output_list, ratio_list
