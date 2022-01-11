from functools import partial

import cv2

from ..shape_filer_constants import POLYGON_FILTER_PRECISION, POLYGON_FILTER_DEFAULT_SIDE_AMOUNT
from ...math.contours import contour_lengths_and_angles
from ..contour_filter import contour_filter
from ...math import geometry
from ...utils.types import RangedNumber


def validate_ratio_against_average(value, value_average, divisor, threshold):
    return 1 - (abs(value - value_average) / divisor) < threshold


def polygon_filter_average(items, precision: int = POLYGON_FILTER_PRECISION):
    return round(sum(items) / float(len(items)), precision)


@contour_filter
def polygon_filter(contour_list, side_amount=POLYGON_FILTER_DEFAULT_SIDE_AMOUNT,
                   angle_deviation: RangedNumber(0, 1) = 0,
                   side_length_deviation: RangedNumber(0, 1) = 0,
                   polygon_fill_ratio: RangedNumber(0, 1) = 0.7,
                   polygon_angle_ratio: RangedNumber(0, 1) = 0,
                   approximation_coefficient: RangedNumber(0, 1) = 0.02):
    """
     A filter that Detects regular polygon of variable amount of sides, default is 6 (Hexagon).
     The filter uses 4 shape characteristics to perform the filtering,
     1. Validate that all sides do not deviate too much from the polygon_filter_average side in the contour
         angle
     2. Validate that all angles do not deviate too much from the polygon_filter_average angle
     3. Validate that angle polygon_filter_average is close to the angle of the polygon with the same amount of sides
     4. Validate that the length of all sides are close to the length of the side of a polygon of a similar size

    :param polygon_angle_ratio:
    :param contour_list: the list of contours to be filtered
    :param side_amount: the amount of sides the wanted polygon has. The Default is to detect a Hexagon
    :param angle_deviation: the minimum ratio between each angle and the polygon_filter_average angle and the polygon_filter_average angle and the
    target angle of a shape of side_amount
    :param polygon_fill_ratio: The minimum ratio between the contour's area and the target area
    :param side_length_deviation: The minimum ratio between the length of each side and the polygon_filter_average length and
    between the polygon_filter_average length.
    :param approximation_coefficient: the coefficient for the function cv2.approxPolyDP.
    :return: the list of contours (numpy ndarrays) that passed the filter and are regular polygon
    """
    if side_amount < 3:
        raise ValueError("A polygon must have at least 3 sides")
    output = []
    ratios = []
    output_append = output.append
    ratio_append = ratios.append
    for current_contour in contour_list:
        vertices, lengths, angles = contour_lengths_and_angles(current_contour, approximation_coefficient)
        if len(vertices) == side_amount:
            average_length = polygon_filter_average(lengths)
            length_validator = partial(validate_ratio_against_average,
                                       average=average_length,
                                       divisor=average_length,
                                       threshold=side_length_deviation)
            if all(map(length_validator, lengths)):
                average_angle = polygon_filter_average(angles)
                angle_validator = partial(validate_ratio_against_average,
                                          average=average_angle,
                                          divisor=average_angle,
                                          threshold=angle_deviation)
                if all(map(angle_validator, angles)):
                    target_angle = geometry.regular_polygon_angle(side_amount)
                    if not validate_ratio_against_average(average_angle,
                                                          target_angle,
                                                          target_angle,
                                                          polygon_angle_ratio):
                        fill_ratio = cv2.contourArea(current_contour) / geometry.polygon_area(average_length,
                                                                                              side_amount)
                        if polygon_fill_ratio <= fill_ratio <= 1 / polygon_fill_ratio:
                            ratio_append(ratios)
                            output_append(current_contour)
    return output, ratios
