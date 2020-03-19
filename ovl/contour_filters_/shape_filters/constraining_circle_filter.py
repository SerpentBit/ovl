import cv2

from ..contour_filter import contour_filter
from ...math_.geometry import circle_fill_ratio


@contour_filter
def constraining_circle_filter(contour_list, min_area_ratio=0.80, min_len_ratio=0.9):
    """
    Filters out contour which are not approximately circle, also limits by radius ratio (unlike circle_filter).
    :param contour_list: list of contours (numpy arrays) to be filtered
    :param min_area_ratio: minimum ratio between the area of the enclosing
                      circle and the contour (contour /enclosing circle)
    :param min_len_ratio: minimum ratio between the radius of the enclosing circle and the enclosing rectangle.
    :return: the list of contours that fit the criteria
    """
    output = []
    ratios = []
    output_append = output.append
    ratio_append = ratios.append
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio, radius = circle_fill_ratio(current_contour)
        _, _, rectangle_width, rectangle_height = cv2.boundingRect(current_contour)
        radius_ratio = ((2 * radius) ** 2) / float(rectangle_width) * rectangle_height
        if min_len_ratio <= (radius_ratio ** 0.5):
            if min_area_ratio <= fill_ratio:
                output_append(current_contour)
                ratio_append((fill_ratio, radius_ratio))
    return output, ratios
