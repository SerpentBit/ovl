import cv2
import warnings

from ..math.contours import open_arc_length, circle_rating

from ..math import image
from .contour_filter import contour_filter
from .sorter_helper_functions import contour_center_and_point_distance


@contour_filter
def area_sort(contour_list, descending_sort=True):
    """
    Sorts the list of contours by contour sort, default is from large to small

    :param contour_list: the list of contours to be sorted, list of ndarrays
    :param descending_sort: a flag that reverses the sort order set to
    :return: the sorted contour list
    """
    return sorted(contour_list, key=cv2.contourArea, reverse=descending_sort)


@contour_filter
def distance_sort(contour_list, point):
    """
    Sorts the contours according to their distance from the
    NOTE: it is important to area filter before image_center_sort

    :param contour_list: The list of contours to be sorted
    :type contour_list: List or one contour (numpy array)
    :param point: the point from which the distance of all contours are sorted by
    :return: the sorted contour list
    """
    return sorted(contour_list,
                  key=contour_center_and_point_distance(point))


@contour_filter
def image_center_sort(contour_list, image_dimensions=(320, 240)):
    """
    Sorts the contours from the closest to the center to the farthest.
    NOTE: it is important to area filter before image_center_sort

    :param contour_list: list of contours to be sorted
    :param image_dimensions: the dimensions of the image
    :return:
    """
    image_center = image.image_center(image_dimensions)
    return sorted(contour_list,
                  key=contour_center_and_point_distance(image_center))


@contour_filter
def dec_area_sort(contour_list):
    """
    Sorts the list of contours from the largest to the smallest based on area of the contour

    :param contour_list: List of Contours to be sorted
    :return: the contour list sorted.
    """
    warnings.warn("dec_area_sort is deprecated, use area_sort() instead", DeprecationWarning)
    return sorted(contour_list, key=lambda x: cv2.contourArea(x), reverse=True)


@contour_filter
def inc_area_sort(contour_list):
    """
    Sorts the list of contours from the smallest to the largest based on area of the contour

    :param contour_list: List of Contours to filter
    :return: the contour list sorted.
    """
    warnings.warn("inc_area_sort is deprecated, use area_sort(descending_sort=False) instead", DeprecationWarning)
    return sorted(contour_list, key=lambda x: cv2.contourArea(x))


@contour_filter
def circle_sort(contour_list, area_limit=0.9, radius_limit=0.8):
    """
    Sorts the list of contours according to how much they are circle from most similar to least
    using the circle rating function.

    :param contour_list: list of Contours to filter
    :type contour_list: list or one contour(numpy array)
    :param area_limit: The area limit for the circle rating, look at Geometry.circle_rating
    :param radius_limit: the radius limit for the circle rating, look at Geometry.circle_rating
    :return: the list sorted by circle rating
    """
    return sorted(contour_list, key=lambda x: circle_rating(x, area_limit, radius_limit))


@contour_filter
def dec_length_sort(contour_list):
    """
    Sorts the list of contours from the largest to the smallest based on area of the contour

    :param contour_list: List of Contours to filter
    :return: the contour list sorted.
    """
    return sorted(contour_list, key=open_arc_length).reverse()


@contour_filter
def inc_length_sort(contour_list):
    """
    Sorts the list of contours from the smallest to the largest based on area of the contour

    :param contour_list: List of Contours to filter
    :return: the contour list sorted.
    """
    return sorted(contour_list, key=open_arc_length)
