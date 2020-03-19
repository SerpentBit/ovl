import cv2

from ..contour_filter import contour_filter
from ...math_ import geometry

@contour_filter
def polygon_filter(contour_list, side_amount=6, min_angle_ratio=0.7,
                   min_area_ratio=0.7, min_len_ratio=0.7, approximation_coefficient=0.02):
    """
     A filter that Detects regular polygon of n-sides sides
    :param contour_list: the list of contours to be filtered
    :param side_amount: the amount of sides the wanted polygon has.
    :param min_angle_ratio: the minimum ratio between the each angle and the average angle and the average angle and the
                            target angle of a shape of side_amount
    :param min_area_ratio: The minimum ratio between the contour's area and the target area
    :param min_len_ratio: The minimum ratio between the length of each side and the average length and
                          between the average length.
    :param approximation_coefficient: the coefficient for the function cv2.approxPolyDP.
    :return: the list of contours (numpy ndarrays) that passed the filter and are regular polygon
    """
    if side_amount < 3:
        raise ValueError("A polygon must have at least 3 sides")
    output = []
    ratios = []
    output_append = output.append
    ratio_append = ratios.append
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        vertices, lengths, angles = geometry.contour_lengths_and_angles(current_contour, approximation_coefficient)
        if len(vertices) == side_amount:
            target_angle = geometry.regular_polygon_angle(side_amount)
            average_length = round(sum(lengths) / float(len(lengths)), 3)
            average_angle = round(sum(angles) / float(len(lengths)), 3)
            for length in lengths:
                if 1 - ((((length - average_length) ** 2) ** 0.5) / average_length) < min_len_ratio:
                    break
            else:
                for angle in angles:
                    if 1 - ((((angle - average_angle) ** 2) ** 0.5) / average_angle) < min_angle_ratio:
                        break
                else:
                    if not 1 - ((((target_angle - average_angle) ** 2) ** 0.5) / target_angle) < min_angle_ratio:
                        ratios = cv2.contourArea(current_contour) / geometry.polygon_area(average_length, side_amount)
                        if min_area_ratio <= ratios <= 1 / min_area_ratio:
                            ratio_append(ratios)
                            output_append(current_contour)
    return output, ratios
