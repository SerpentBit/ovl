import cv2

from ovl import contour_filter, rectangle_fill_ratio_straight


@contour_filter
def straight_square_filter(contour_list, min_area_ratio=0.8, min_len_ratio=0.95):
    """
    Receives a list of contours and returns
    only the ones that are approximately square
    Relation checked is [minimum ratio < (Circle radius / width * height * (square root of 2)) < maximum ratio]
    :param contour_list: List of Contours to filter
    :type contour_list: List
    :param min_len_ratio: maximum ratio between radius and sides of bounding rectangle
    :param min_area_ratio: the minimum ratio between the area of the contour and the area of the bounding shape
    :return: the contour list filtered.
     """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio, contour_width, contour_height = rectangle_fill_ratio_straight(current_contour)
        peri = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approximation) == 4:
            _, enclosing_radius = cv2.minEnclosingCircle(current_contour)
            bounding_rectangle_diagonal = (2 ** 0.5) * ((contour_width * contour_height) ** 2)
            enclosing_circle_radius = 2 * enclosing_radius
            radius_ratio = enclosing_circle_radius / bounding_rectangle_diagonal
            if radius_ratio >= min_len_ratio:
                output_list.append(current_contour)
                ratio_list.append(fill_ratio * radius_ratio)
    return output_list, ratio_list