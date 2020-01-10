from functools import partial

from ..math_ import geometry


def contour_and_point_distance(point):
    """
    A reusable function that preloads a point and then
    calculates the distance to a given contour.
    :param point: an (x,y) tuple point
    :return:
    """
    return partial(geometry.distance_between_points, point)
