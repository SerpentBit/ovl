import cv2

from ovl import contour_filter, rectangle_fill_ratio_straight


@contour_filter
def straight_rectangle_filter(contour_list, min_area_ratio=0.8):
    """
    Receives a list of contours and returns only those that are approximately a rectangle that
    its sides are parallel to the frame of the image

    :param contour_list: List of Contours to filter
    :type contour_list: List
    :param min_area_ratio: The minimum ratio between the rectangle and the contour
    :type min_area_ratio: float
    :return: the contour list filtered.
     """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio, _, _ = rectangle_fill_ratio_straight(current_contour)
        perimeter = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * perimeter, True)
        if fill_ratio > min_area_ratio and len(approximation) == 4:
            output_list.append(current_contour)
            ratio_list.append(fill_ratio)
    return output_list, ratio_list