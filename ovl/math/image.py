import numpy as np

from .contours import contour_center
from .geometry import slope, x_intersection, y_intersection, distance_between_points


def image_center(image_dimensions):
    """
    Calculates the center pixels of a given image dimension

    :param image_dimensions: (width, height) tuple of the size of the image
    :return: the (x, y) center of the image
    """
    return tuple(map(lambda dimension: dimension / 2, image_dimensions))


def distance_from_frame(point, image_dimensions):
    """
    Calculates the distance of a given point from the frame of the image based on the vector from the center
    and the point

    :param point: point (x,y tuple) or contour (numpy array)
    :param image_dimensions: the size of the image, (width, height)
    :return: the distance
    """
    point = contour_center(point) if type(point) is np.ndarray else point
    center_of_image = image_center(image_dimensions)
    line_slope = slope(point, center_of_image)
    intercept = - line_slope * point[0] + point[1]
    xs = (image_dimensions[0] - 1, 0)
    ys = (image_dimensions[1] - 1, 0)
    y_distances = [distance_between_points(y_intersection(line_slope, intercept, y), point) for y in ys]
    x_distances = [distance_between_points(x_intersection(line_slope, intercept, x), point) for x in xs]
    return min(y_distances + x_distances)


def image_size(image: np.ndarray) -> int:
    """
    Calculates the size of the given image in pixels

    :param image: ndarray image in pixels
    :return: the image size
    """
    return image.shape[0] * image.shape[1]
