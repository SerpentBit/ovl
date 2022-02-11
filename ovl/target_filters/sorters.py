import cv2

from .contour_filter import target_filter
from .sorter_helper_functions import contour_center_and_point_distance
from ..math import image
from ..math.contours import open_arc_length, circle_rating
from ..utils.constants import DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT


@target_filter
def area_sort(contour_list, descending_sort=True):
    """
    Sorts the list of contours by contour sort, default is from large to small

    :param contour_list: the list of contours to be sorted, list of ndarrays
    :param descending_sort: a flag that reverses the sort order set to
    :return: the sorted contour list
    """
    return sorted(contour_list, key=cv2.contourArea, reverse=descending_sort)


@target_filter
def distance_sort(contour_list, point):
    """
    Sorts the contours according to their distance from the
    NOTE: it is important to area filter before distance_sort

    :param contour_list: The list of contours to be sorted
    :type contour_list: List or one contour (numpy array)
    :param point: the point from which the distance of all contours are sorted by
    :return: the sorted contour list
    """
    return sorted(contour_list, key=contour_center_and_point_distance(point))


@target_filter
def image_center_sort(contour_list, image_dimensions=(DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT)):
    """
    Sorts the contours from the closest to the center to the farthest.
    NOTE: it is important to area filter before image_center_sort

    :param contour_list: list of contours to be sorted
    :param image_dimensions: the dimensions of the image
    :return:
    """
    image_center = image.image_center(image_dimensions)
    return sorted(contour_list, key=contour_center_and_point_distance(image_center))


@target_filter
def circle_sort(contour_list, area_limit=0.9, radius_limit=0.8):
    """
    Sorts the list of contours according to how similar they are to a circle from most similar to least
    using the circle rating function.

    :param contour_list: list of Contours to filter
    :type contour_list: list or one contour(numpy array)
    :param area_limit: The area limit for the circle rating, look at Geometry.circle_rating
    :param radius_limit: the radius limit for the circle rating, look at Geometry.circle_rating
    :return: the list sorted by circle rating
    """
    return sorted(contour_list, key=lambda x: circle_rating(x, area_limit, radius_limit))


@target_filter
def length_sort(contour_list, descending_sort=True):
    """
    Sorts the list of contours from the longest to the shortest based on length of the contour (for open contours)

    :param contour_list: List of Contours to filter
    :param descending_sort: true if the sort is from longest to shortest contour, False reverses it
    :return: the contour list sorted.
    """
    return sorted(contour_list, key=open_arc_length,reverse=descending_sort)
