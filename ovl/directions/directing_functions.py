from numpy import ndarray

from ..math import contours as contours_


def xy_center_directions(contours, image: ndarray):
    """
    Returns the direction the detect objects (contours) are compared to the center
    of the image, this is returned in normalized screen space -1 to 1 (-1 meaning the most left compared to the center,
    and 1 the most right compared to the center and 0 meaning perfectly centered

    xy_center_directions returns x and y center directions,

    For example:
    If the center of the targets are the center of the image (width / 2, height / 2)
    the returned values are 0 and 0 meaning the camera is centered on the target


    :param contours: the final contours found after filtering - your targets
    :param image: the image from which it was found
    :return: the normalized screen space x and y coordinates of your final targets
    """
    return contours_.calculate_normalized_screen_space(contours, image)


def center_directions(contours, image: ndarray):
    """
    Returns the average center of the contours
    or list of contours that are the final targets

    This is the default directions function since it
    doesnt calculate any directions, only finds the center

    :param contours: the final contours - your targets
    :param image: the image from which it was found
    """
    return contours_.contour_average_center(contours)


def target_amount_directions(contours, image: ndarray):
    """
    Counts the amount of successful object detections.

    :param contours: the final contours - your targets
    :param image: the image from which it was found
    :return: the amount of targets detected
    """
    return len(contours)
