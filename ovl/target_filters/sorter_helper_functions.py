from functools import partial

from ..ovl_math import contours
from ..ovl_math import geometry


def contour_and_point_distance(point):
    """
    A reusable function that preloads a point and then
    calculates the distance to a given contour.
    :param point: an (x,y) tuple point
    :return:
    """
    return partial(geometry.distance_between_points, point)


def contour_center_and_point_distance(point):
    def contour_center_distance(contour, second_point):
        return geometry.distance_between_points(contours.contour_center(contour), second_point)
    return partial(contour_center_distance, point)
