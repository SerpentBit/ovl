# Copyright 2018 Ori Ben-Moshe - All rights reserved.
import cv2
from . import Geometry
from sys import version_info

if version_info[0] == 3:
    xrange = range


def dec_area_sort(contour_list):
    """
    Action: sorts the list of contours from the largest to the smallest based on area of the contour
    :param contour_list: List of Contours to filter
    :type contour_list: List or one contour (ndarray)
    :return: the contour list sorted.
    """
    if type(contour_list) is not list:
        return [contour_list]
    contour_list = sorted(contour_list, key=lambda x: cv2.contourArea(x))[::-1]
    return contour_list


def inc_area_sort(contour_list):
    """
    Action: sorts the list of contours from the smallest to the largest based on area of the contou
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
