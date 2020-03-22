from ..math_.geometry import *
from ..math_.geometry import distance_between_points as dbp, distance_from_frame as dff
from .contour_filter import contour_filter
from ..helpers_.types import RangedNumber


@contour_filter
def image_center_filter(contour_list, image_dimensions: typing.Tuple[int, int] = (320, 240),
                        max_dist: RangedNumber(0, 1) = 0.7):
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
    for current_contour in contour_list:
        current_contour_center = contour_center(current_contour)
        distance_ratio = (dbp(current_contour_center, image_center)
                          / float(dff(current_contour_center, image_dimensions)))
        if distance_ratio >= max_dist:
            output.append(current_contour)
            ratio.append(distance_ratio)
    return output, ratio


@contour_filter
def distance_filter(contour_list, point: typing.Tuple[int, int], min_dist: float = 0, max_dist: float = 50):
    """
    Filters out contours that their center is not close enough
    to the given (x, y) point in the image
    :param contour_list: a list of contours to be filtered
    :param point: the point from which the contours should be filtered a tuple (or list) of 2 numbers.
    :param max_dist: the maximum distance from the point in pixels
    :param min_dist: the minimum distance from the point in pixels
    :return: the filtered contour list
    """
    output = []
    ratio = []
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
    Filters out contours that their center is not close enough
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
    Receives a list of contours and removes ones that are not long enough
    Note: for "open" contours only!
    :param contour_list: list of contours (numpy array) to be filtered
    :param min_length: minimum length of a contour (in pixels)
    :param max_length: maximum length of a contour (in pixels)
    :return: list of filtered contours and list of the lengths
    """
    output = []
    ratio = []
    for current_contour in contour_list:
        perimeter = cv2.arcLength(current_contour, False)
        if min_length >= perimeter >= max_length:
            output.append(current_contour)
            ratio.append(perimeter)
    return output, ratio


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
    for current_contour in contour_list:
        if min_area <= cv2.contourArea(current_contour) <= max_area:
            output_list.append(current_contour)
            ratio_list.append(current_contour)
    return output_list, ratio_list


@contour_filter
def percent_area_filter(contour_list, minimal_percent: RangedNumber(0, 1) = 0.002,
                        maximum_percent: RangedNumber(0, 1) = 1, image_dimensions: Tuple[int, int] = (320, 240)):
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
