import cv2

from ..target_filter import target_filter
from ...ovl_math.shape_fill_ratios import rotating_rectangle_fill_ratio
from ...utils.types import RangedNumber


@target_filter
def rotated_square_filter(contour_list, min_area_ratio: RangedNumber(0, 1) = 0.8, min_ratio: RangedNumber(0, 1) = 0.95,
                          max_ratio: RangedNumber(0, 1) = 1.05):
    """
    Receives a list of contours
    and returns only the ones that are approximately square
    Relation checked is [minimum ratio < (Circle radius / width * height * (square root of 2)) < maximum ratio]

    :param contour_list: List of Contours to filter
    :param max_ratio: maximum ratio between radius and sides of bounding rectangle
    :param min_ratio: minimum ratio between radius and sides of bounding rectangle
    :param min_area_ratio: minimum ratio between the area of the contours and the bounding shape
    :return: the contour list filtered.
    """
    ratio_list = []
    output_list = []
    for current_contour in contour_list:
        fill_ratio, bounding_width, bounding_height = rotating_rectangle_fill_ratio(current_contour)
        _, enclosing_radius = cv2.minEnclosingCircle(current_contour)
        contour_perimeter = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * contour_perimeter, True)
        if fill_ratio > min_area_ratio and len(approximation) == 4:
            diagonal_length = (2 ** 0.5) * ((bounding_width * bounding_height) ** 0.5)
            enclosing_circle_diameter = 2 * enclosing_radius
            radius_ratio = enclosing_circle_diameter / diagonal_length
            if min_ratio < radius_ratio < max_ratio:
                output_list.append(current_contour)
                if radius_ratio > 1:
                    radius_ratio = 1 / radius_ratio
                ratio_list.append(fill_ratio * radius_ratio)
    return output_list, ratio_list
