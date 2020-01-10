# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
from typing import List

from ..math_.geometry import *
from ..math_.geometry import distance_between_points as dbp, distance_from_frame as dff
from .contour_filter import contour_filter


@contour_filter
def image_center_filter(contour_list, image_dimensions=(320, 240), max_dist=0.7):
    """
     Filters out contours that their center is not close enough to the center of the image
    :param contour_list: a list of contours to be filtered
    :param image_dimensions: the size of the image(width, height)
    :param max_dist: the maximum percent of difference
    :return: list of contours within the maximum distance from the image center
    """
    output = []
    ratio = []
    image_center = (image_dimensions[0] / 2 - .5, image_dimensions[1] / 2 - .5)
    if type(contour_list) is not list:
        contour_list = [contour_list]

    for current_contour in contour_list:
        current_contour_center = contour_center(current_contour)
        distance_ratio = (dbp(current_contour_center, image_center)
                          / float(dff(current_contour_center, image_dimensions)))
        if distance_ratio >= max_dist:
            output.append(current_contour)
            ratio.append(distance_ratio)
    return output, ratio


@contour_filter
def distance_filter(contour_list, point, min_dist=0, max_dist=50):
    """
     filters out contours that their center is not close enough
            to the given (x, y) point
    :param contour_list: a list of contours to be filtered
    :param point: the point from which the contours should be filtered a tuple (or list) of 2 numbers.
    :param max_dist: the maximum distance from the point in pixels
    :param min_dist: the minimum distance from the point in pixels
    :return: the filtered contour list
    """
    output = []
    ratio = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        current_contour_center = contour_center(current_contour)
        distance_from_center = dbp(current_contour_center, point)
        if max_dist >= distance_from_center >= min_dist:
            output.append(current_contour)
            ratio.append(distance_from_center)
    return output, ratio


@contour_filter
def absolute_distance_filter(contour_list, max_dist=50, min_dist=0, image_dimensions=(320, 240)):
    """
     filters out contours that their center is not close enough
            to the center of the image
    :param contour_list: a list of contours to be filtered
    :param image_dimensions: the size of the image(width, height)
    :param max_dist: the maximum distance from the center in pixels
    :param min_dist: the minimum distance from the center in pixels
    :return:
    """
    output = []
    ratio = []
    image_center = (image_dimensions[0] / 2 - .5, image_dimensions[1] / 2 - .5)
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        current_contour_center = contour_center(current_contour)
        distance_from_center = dbp(current_contour_center, image_center)
        if max_dist >= distance_from_center >= min_dist:
            output.append(current_contour)
            ratio.append(distance_from_center)
    return output, ratio


@contour_filter
def length_filter(contour_list, min_length=50, max_length=76800):
    """
     receives a list of contours and removes ones that are not long enough
            Note: for "open" contours!
    :param contour_list: list of contours (numpy array) to be filtered
    :param min_length: minimum length of a contour (in pixels)
    :param max_length: maximum length of a contour (in pixels)
    :return: list of filtered contours and list of the lengths
    """
    output = []
    ratio = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        perimeter = cv2.arcLength(current_contour, False)
        if min_length >= perimeter >= max_length:
            output.append(current_contour)
            ratio.append(perimeter)
    return output, ratio


@contour_filter
def straight_square_filter(contour_list, min_area_ratio=0.8, min_len_ratio=0.95):
    """
     receives a list of contours
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
    for current_contour in contour_list:
        fill_ratio, contour_width, contour_height = rectangle_fill_ratio_straight(current_contour)
        peri = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approximation) == 4:
            _, enclosing_radius = cv2.minEnclosingCircle(current_contour)
            bounding_rectangle_diagonal = (2 ** 0.5) * ((contour_width * contour_height) ** 2)
            enclosing_circle_radius = 2 * enclosing_radius
            radius_ratio = enclosing_circle_radius / bounding_rectangle_diagonal
            if radius_ratio >= min_len_ratio:
                output_list.append(current_contour)
                ratio_list.append(fill_ratio * radius_ratio)
    return output_list, ratio_list


@contour_filter
def rotated_square_filter(contour_list, min_area_ratio=0.8, min_ratio=0.95, max_ratio=1.05):
    """
     receives a list of contours
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


@contour_filter
def vertical_rectangle_filter(contour_list, min_area_ratio=0.):
    """
     receives a list of contours
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
    for current_contour in contour_list:
        fill_ratio, contour_width, contour_height = rectangle_fill_ratio_straight(current_contour)
        peri = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and contour_width < contour_height and len(approximation) == 4:
            output_list.append(current_contour)
            ratio_list.append(fill_ratio)
    return output_list, ratio_list


@contour_filter
def horizontal_rectangle_filter(contour_list, min_area_ratio=0.8):
    """
     receives a list of contours and returns only those that are approximately a horizontal rectangle
    :param contour_list: List of Contours to filter
    :type contour_list: List
    :param min_area_ratio
    :return: the contour list filtered.
     """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio, contour_width, contour_height = rectangle_fill_ratio_straight(current_contour)
        perimeter = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * perimeter, True)
        if fill_ratio > min_area_ratio and contour_width > contour_height and len(approximation) == 4:
            output_list.append(current_contour)
            ratio_list.append(fill_ratio)
    return output_list, ratio_list


@contour_filter
def area_filter(contour_list, min_area=200, max_area=math.inf):
    """
    Filters contours that are not within the threshold of area (in pixels)
    :param max_area: maximum area of a contour (Inclusive) default is no limit (infinity)
    :param min_area: minimum area of a contour (Inclusive) set to 0 for no lower limit.
    :param contour_list: List of Contours to filter
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


@contour_filter
def straight_rectangle_filter(contour_list, min_area_ratio=0.8):
    """
     receives a list of contours and returns only those that are approximately a rectangle
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
    for current_contour in contour_list:
        fill_ratio, _, _ = rectangle_fill_ratio_straight(current_contour)
        perimeter = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * perimeter, True)
        if fill_ratio > min_area_ratio and len(approximation) == 4:
            output_list.append(current_contour)
            ratio_list.append(fill_ratio)
    return output_list, ratio_list


@contour_filter
def rotated_rectangle_filter(contour_list, min_area_ratio=0.8):
    """
    receives a list of contours and returns only those that are approximately a rectangle regardless
    of the angle of rotation.
    :param contour_list: List of Contours to filter
    :param min_area_ratio: the minimum ratio between the contour area and the bounding shape
    :return: the contour list filtered.
     """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio, w, h = rotating_rectangle_fill_ratio(current_contour)
        peri = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approximation) == 4:
            ratio_list.append(fill_ratio)
            output_list.append(current_contour)
    return output_list, ratio_list


@contour_filter
def triangle_filter(contour_list, min_area_ratio=0.8):
    """
    Receives a list of contours and returns only those that are approximately
    triangle
    :param contour_list: the list of contours to be filtered
    :param min_area_ratio: the minimum ratio between the area of the contour and the bounding triangle
    :return: the filtered list
    """
    output_list = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio = triangle_fill_ratio(current_contour)
        peri = cv2.arcLength(current_contour, True)
        approximation = cv2.approxPolyDP(current_contour, 0.02 * peri, True)
        if fill_ratio > min_area_ratio and len(approximation) == 3:
            ratio_list.append(fill_ratio)
            output_list.append(current_contour)
    return output_list, ratio_list


@contour_filter
def circle_filter(contour_list, min_area_ratio=0.7):
    """
    filters out contour which are not approximately circle.
    :param contour_list: list of contours (numpy arrays) to be filtered
    :param min_area_ratio: minimum ratio between the area of the enclosing
                         circle and the contour (contour /enclosing circle)
    :return: the list of contours that fit the criteria
    """
    output = []
    ratio_list = []
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio, radius = circle_fill_ratio(current_contour)
        if min_area_ratio <= fill_ratio:
            output.append(current_contour)
            ratio_list.append(fill_ratio)
    return output, ratio_list


@contour_filter
def constraining_circle_filter(contour_list, min_area_ratio=0.80, min_len_ratio=0.9):
    """
    Filters out contour which are not approximately circle, also limits by radius ratio (unlike circle_filter).
    :param contour_list: list of contours (numpy arrays) to be filtered
    :param min_area_ratio: minimum ratio between the area of the enclosing
                      circle and the contour (contour /enclosing circle)
    :param min_len_ratio: minimum ratio between the radius of the enclosing circle and the enclosing rectangle.
    :return: the list of contours that fit the criteria
    """
    output = []
    ratios = []
    output_append = output.append
    ratio_append = ratios.append
    if type(contour_list) is not list:
        contour_list = [contour_list]
    for current_contour in contour_list:
        fill_ratio, radius = circle_fill_ratio(current_contour)
        _, _, rectangle_width, rectangle_height = cv2.boundingRect(current_contour)
        radius_ratio = ((2 * radius) ** 2) / float(rectangle_width) * rectangle_height
        if min_len_ratio <= (radius_ratio ** 0.5):
            if min_area_ratio <= fill_ratio:
                output_append(current_contour)
                ratio_append((fill_ratio, radius_ratio))
    return output, ratios


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
        vertices, lengths, angles = contour_lengths_and_angles(current_contour, approximation_coefficient)
        if len(vertices) == side_amount:
            target_angle = regular_polygon_angle(side_amount)
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
                        ratios = cv2.contourArea(current_contour) / polygon_area(average_length, side_amount)
                        if min_area_ratio <= ratios <= 1 / min_area_ratio:
                            ratio_append(ratios)
                            output_append(current_contour)
    return output, ratios


@contour_filter
def percent_area_filter(contour_list, minimal_percent=0.002, maximum_percent=1, image_dimensions=(320, 240)):
    """
    Filters out contours that are not in the specified ratio to the area of the image (1% -> 0.1)
    :param contour_list: list of contours to be filtered (numpy.ndarray)
    :param minimal_percent: the minimal ratio between the contour area and the image area
    :param maximum_percent: the maximum ratio between the contour area and the image area
    :param image_dimensions: The (width, height) of the image in pixels,
    :return:
    """
    output = []
    ratios = []
    output_append = output.append
    ratio_append = ratios.append
    image_size = image_dimensions[0] * image_dimensions[1]
    if image_size == 0:
        raise ValueError("Invalid image dimensions, Received (width, height): {}, {}".format(*image_dimensions))
    for current_contour in contour_list:
        contour_area = cv2.contourArea(current_contour)
        percent_area = contour_area / image_size
        if minimal_percent <= percent_area <= maximum_percent:
            ratio_append(percent_area)
            output_append(current_contour)
    return output, ratios
