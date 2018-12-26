# Copyright 2018 Ori Ben-Moshe - All rights reserved.
import cv2
import Geometry
from General import root
from sys import version_info
from numpy import mean, std

if version_info[0] == 3:
    xrange = range


def straight_square_filter(contour_list, min_area_ratio=0.8, min_len_ratio=0.95):
    """
    Action: receives a list of contours
    and returns only the ones that are approximately square
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
    for currentContour in contour_list:
        fill_ratio, w, h = Geometry.get_fill_ratio_straight(currentContour)
        peri = cv2.arcLength(currentContour, True)
        approx = cv2.approxPolyDP(currentContour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approx) == 4:
            _, enclosing_radius = cv2.minEnclosingCircle(currentContour)
            p1 = root(2, 2) * root(w * h, 2)
            p2 = 2 * enclosing_radius
            radius_ratio = p2 / p1
            if radius_ratio >= min_len_ratio:
                output_list.append(currentContour)
                ratio_list.append(fill_ratio * radius_ratio)
    return output_list, ratio_list


def rotated_square_filter(contour_list, min_area_ratio=0.8, min_ratio=0.95, max_ratio=1.05):
    """
    Action: receives a list of contours
    and returns only the ones that are approximately square
    Relation checked is [minimum ratio < (Circle radius / width * height * (square root of 2)) < maximum ratio]
    :param contour_list: List of Contours to filter
    :param max_ratio: maximum ratio between radius and sides of bounding rectangle
    :type max_ratio: float
    :param min_ratio: minimum ratio between radius and sides of bounding rectangle
    :type min_ratio: float
    :param min_area_ratio: minimum ratio between the area of the contours and the bounding shape
    :return: the contour list filtered.
     """
    ratio_list = []
    output_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for currentContour in contour_list:
        fill_ratio, w, h = Geometry.get_fill_ratio_rotating(currentContour)
        _, enclosing_radius = cv2.minEnclosingCircle(currentContour)
        peri = cv2.arcLength(currentContour, True)
        approx = cv2.approxPolyDP(currentContour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approx) == 4:
            p1 = root(2, 2) * root(w * h, 2)
            p2 = 2 * enclosing_radius
            radius_ratio = p2 / p1
            if min_ratio < radius_ratio < max_ratio:
                output_list.append(currentContour)
                if radius_ratio > 1:
                    radius_ratio = 1 / radius_ratio
                ratio_list.append(fill_ratio * radius_ratio)
    return output_list, ratio_list


def vertical_rectangle_filter(contour_list, min_area_ratio=0.):
    """
    Action: receives a list of contours
    and returns only the ones that are approximately a vertical rectangle
    :param contour_list: List of Contours to filter
    :type contour_list: List
    :param min_area_ratio: minimum ratio between the area of the contours and the bounding shape
    :return: the contour list filtered.
     """
    ratio_list = []
    output_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for currentContour in contour_list:
        fill_ratio, w, h = Geometry.get_fill_ratio_straight(currentContour)
        peri = cv2.arcLength(currentContour, True)
        approx = cv2.approxPolyDP(currentContour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and w < h and len(approx) == 4:
            output_list.append(currentContour)
            ratio_list.append(fill_ratio)
    return output_list, ratio_list


def horizontal_rectangle_filter(contour_list, min_area_ratio=0.8):
    """
    Action: receives a list of contours and returns only those that are approximately a horizontal rectangle
    :param contour_list: List of Contours to filter
    :type contour_list: List
    :param min_area_ratio
    :return: the contour list filtered.
     """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for currentContour in contour_list:
        fill_ratio, w, h = Geometry.get_fill_ratio_straight(currentContour)
        peri = cv2.arcLength(currentContour, True)
        approx = cv2.approxPolyDP(currentContour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and w > h and len(approx) == 4:
            output_list.append(currentContour)
            ratio_list.append(fill_ratio)
    return output_list, ratio_list


def area_filter(contour_list, min_area=200, max_area=76800):
    """
    Action: filters contours that are not within the threshold of area

    :param max_area: maximum area of a contour (Inclusive) set to the size of the image for no upper limit.
    :param min_area: minimum area of a contour (Inclusive) set to 0 for no lower limit.
    :param contour_list: List of Contours to filter
    :type contour_list: List
    :return: the contour list filtered.
    """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        if min_area <= cv2.contourArea(current_contour) <= max_area:
            output_list.append(current_contour)
            ratio_list.append(current_contour)
    return output_list, ratio_list


def straight_rectangle_filter(contour_list, min_area_ratio=0.8):
    """
    Action: receives a list of contours and returns only those that are approximately a rectangle
    and that are not rotated

    :param contour_list: List of Contours to filter
    :type contour_list: List
    :param min_area_ratio: The minimum ratio between the rectangle and the contour
    :type min_area_ratio: float
    :return: the contour list filtered.
     """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for currentContour in contour_list:
        fill_ratio, _, _ = Geometry.get_fill_ratio_straight(currentContour)
        peri = cv2.arcLength(currentContour, True)
        approx = cv2.approxPolyDP(currentContour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approx) == 4:
            output_list.append(currentContour)
            ratio_list.append(fill_ratio)
    return output_list, ratio_list


def rotated_rectangle_filter(contour_list, min_area_ratio):
    """
    Action: receives a list of contours and returns only those that are approximately a rectangle regardless
    of the angle of rotation.
    :param contour_list: List of Contours to filter
    :type contour_list: List
    :param min_area_ratio: the minimum ratio between the contour area and the bounding shape
    :return: the contour list filtered.
     """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for currentContour in contour_list:
        fill_ratio, w, h = Geometry.get_fill_ratio_rotating(currentContour)
        peri = cv2.arcLength(currentContour, True)
        approx = cv2.approxPolyDP(currentContour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approx) == 4:
            ratio_list.append(fill_ratio)
            output_list.append(currentContour)
    return output_list, ratio_list


def triangle_filter(contour_list, min_area_ratio=0.8):
    """
    Action: receives a list of contours and returns only those that are approximately
    traingle
    :param contour_list:
    :param min_area_ratio:
    :return:
    """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for currentContour in contour_list:
        fill_ratio = Geometry.get_fill_ratio_triangle(currentContour)
        peri = cv2.arcLength(currentContour, True)
        approx = cv2.approxPolyDP(currentContour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approx) == 3:
            ratio_list.append(fill_ratio)
            output_list.append(currentContour)
    return output_list, ratio_list


def circle_filter(contour_list, min_area_ratio=0.80, min_len_ratio=0.9):
    """
    Action: filters out contour which are not approximately circle.
    :param contour_list: list of arrays (numpy uint8 ndarrays (contours) to be filtered
    :param min_area_ratio: minimum ratio between the area of the enclosing
                      circle and the contour (contour /enclosing circle)
    :param min_len_ratio: minimum ratio between the radius of the enclosing circle and the enclosing rectangle.
    :return: the list of contours that fit the criteria
    """
    output = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for currentContour in contour_list:
        fill_ratio, radius = Geometry.get_fill_ratio_circle(currentContour)
        _, _, w, h = cv2.boundingRect(currentContour)
        radius_ratio = ((2 * radius) ** 2) / float(w) * h
        if min_len_ratio <= root(radius_ratio, 2):
            if min_area_ratio <= fill_ratio:
                output.append(currentContour)
                ratio_list.append((fill_ratio, radius_ratio))
    return output, ratio_list


def regular_polygon_filter(contour_list,
                           side_amount=6,
                           min_angle_ratio=0.9,
                           min_area_ratio=0.85,
                           min_len_ratio=0.9,
                           approx_coef=0.02):
    """
    Action: A filter that Detects regular polygon of n-sides sides
    :param contour_list: the list of contours to be filtered
    :param side_amount: the amount of sides the wanted polygon has.
    :param min_angle_ratio: the minimum ratio between the each angle and the average angle and the average angle and the
                            target angle of a shape of side_amount
    :param min_area_ratio: The minimum ratio between the contour's area and the target area
    :param min_len_ratio: The minimum ratio between the length of each side and the average length and
                          between the average length.
    :param approx_coef: the coefficient for the function cv2.approxPolyDP.
    :return:
    """
    if side_amount < 3:
        return []
    output = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for currentContour in contour_list:
        vertices, lengths, angles = Geometry.get_lengths_and_angles(currentContour, approx_coef)
        if len(vertices) == side_amount:
            target_angle = Geometry.n_polygon_angle(side_amount)
            average_length = round(sum(lengths) / float(len(lengths)), 3)
            average_angle = round(sum(angles) / float(len(lengths)), 3)
            invalid_value = False
            for length in lengths:
                if 1 - (root((length - average_length)**2, 2) / average_length) < min_len_ratio:
                    invalid_value = True
                    break
            if not invalid_value:
                for angle in angles:
                    if 1 - (root((angle - average_angle)**2, 2) / average_angle) < min_angle_ratio:
                        invalid_value = True
                        break
                if not invalid_value:
                    if 1 - (root((target_angle - average_angle)**2, 2) / target_angle) < min_angle_ratio:
                        invalid_value = True
                    if not invalid_value:
                        ratio = cv2.contourArea(currentContour) / Geometry.n_polygon_area(average_length, side_amount)
                        if min_area_ratio <= ratio <= 1 / min_area_ratio:
                            ratio_list.append(ratio)
                            output.append(currentContour)
    return output, ratio_list
