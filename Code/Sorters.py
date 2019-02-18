# Copyright 2018 - 2019 Ori Ben-Moshe - All rights reserved.
import cv2
from . import Geometry
from sys import version_info

if version_info[0] == 3:
    xrange = range


def image_center_sort(contour_list, image_dimensions=(320, 240)):
    """
    Action: sorts the contours from the closest to the center to the farthest.
    NOTE: it is important to area filter before image_center_sort
    :param contour_list: list of contours to be sorted
    :type contour_list: List or one contour (ndarray)
    :param image_dimensions: the dimensions of the image
    :return:
    """
    if type(contour_list) is not list:
        return [contour_list]
    image_center = ((image_dimensions[0] - 1) / 2, (image_dimensions[1] - 1) / 2)
    return sorted(contour_list,
                  key=lambda x: Geometry.distance_between_points(image_center, Geometry.get_contour_center(x)))


def dec_area_sort(contour_list):
    """
    Action: sorts the list of contours from the largest to the smallest based on area of the contour
    :param contour_list: List of Contours to be sorted
    :type contour_list: List or one contour (ndarray)
    :return: the contour list sorted.
    """
    if type(contour_list) is not list:
        return [contour_list]
    contour_list = sorted(contour_list, key=lambda x: cv2.contourArea(x))[::-1]
    return contour_list


def inc_area_sort(contour_list):
    """
    Action: sorts the list of contours from the smallest to the largest based on area of the contour
    :param contour_list: List of Contours to filter
    :type contour_list: List or one contour (ndarray)
    :return: the contour list sorted.
    """
    if type(contour_list) is not list:
        return [contour_list]
    contour_list = sorted(contour_list, key=lambda x: cv2.contourArea(x))
    return contour_list


def circle_sort(contour_list, area_limit=0.9, radius_limit=0.8):
    """
    Action: sorts the list of contours according to how much they are circle from most similar to least
            using the circle rating function.
    :param contour_list: list of Contours to filter
    :type contour_list: list or one contour(ndarray)
    :param area_limit: The area limit for the circle rating, look at Geometry.circle_rating
    :param radius_limit: the radius limit for the circle rating, look at Geometry.circle_rating
    :return: the list sorted by circle rating
    """
    if type(contour_list) is not list:
        return [contour_list]
    contour_list = sorted(contour_list, key=lambda x: Geometry.circle_rating(x, area_limit, radius_limit))
    return contour_list


def dec_length_sort(contour_list):
    """
    Action: sorts the list of contours from the largest to the smallest based on area of the contour
    :param contour_list: List of Contours to filter
    :type contour_list: List or one contour (ndarray)
    :return: the contour list sorted.
    """
    if type(contour_list) is not list:
        return [contour_list]
    contour_list = sorted(contour_list, key=Geometry.open_arc_length)[::-1]
    return contour_list


def inc_length_sort(contour_list):
    """
    Action: sorts the list of contours from the smallest to the largest based on area of the contour
    :param contour_list: List of Contours to filter
    :type contour_list: List or one contour (ndarray)
    :return: the contour list sorted.
    """
    if type(contour_list) is not list:
        return [contour_list]
    contour_list = sorted(contour_list, key=Geometry.open_arc_length)
    return contour_list
