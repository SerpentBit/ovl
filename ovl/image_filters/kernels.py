import cv2
import numpy as np


def valid_odd_size(size):
    """
    Validates that a kernel shape is of odd ints and of with 2 dimensions

    :param size: the shape (size) to be checked
    :return: False if size is invalid
    """
    if type(size) not in (list, tuple):
        return False
    if len(size) != 2:
        return False
    if size[0] % 2 != 1 or size[1] % 2 != 1:
        return False
    return True


def cross_kernel(size):
    r"""
    Returns a cross (ones in a cross) kernel for morphological functions
    Example of a (5,5) cross:

    | \| 0 0 1 0 0  \|
    | \| 0 0 1 0 0  \|
    | \| 1 1 1 1 1  \|
    | \| 0 0 1 0 0  \|
    | \| 0 0 1 0 0  \|

    :param size:  a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the `numpy.array` of the cross shape
    """
    if not valid_odd_size(size):
        raise ValueError(f"Invalid kernel size given, make sure the size (width, height) are both positive and odd,"
                         f" size given {size}")
    return cv2.getStructuringElement(cv2.MORPH_CROSS, ksize=size)


def rectangle_kernel(size):
    r"""
    Returns a rectangle (all ones) kernel for morphological functions
    Example of a (5,5) rectangle:

    | \| 1 1 1 1 1 \|
    | \| 1 1 1 1 1 \|
    | \| 1 1 1 1 1 \|
    | \| 1 1 1 1 1 \|
    | \| 1 1 1 1 1 \|

    :param size: a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the `numpy.array` of the cross shape
    """
    return cv2.getStructuringElement(cv2.MORPH_RECT, ksize=size)


def ellipse_kernel(size):
    r"""
    Returns an ellipse (ones in the shape of an ellipse) kernel for morphological functions
    Example of a (5,5) ellipse:

    | \| 0 0 1 0 0 \|
    | \| 1 1 1 1 1 \|
    | \| 1 1 1 1 1 \|
    | \| 1 1 1 1 1 \|
    | \| 0 0 1 0 0 \|

    :param size: a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the kernel
    """
    if not valid_odd_size(size):
        raise ValueError(f"Invalid kernel size given, make sure the size (width, height) are both positive and odd,"
                         f" size given {size}")
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=size)


def horizontal_line_kernel(size):
    r"""
    Returns a horizontal line (a horizontal line of ones) kernel for morphological functions
    Example of a (5,5) horizontal line:

    | \| 0 0 0 0 0 \|
    | \| 0 0 0 0 0 \|
    | \| 1 1 1 1 1 \|
    | \| 0 0 0 0 0 \|
    | \| 0 0 0 0 0 \|

    :param size: a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the kernel
    """
    if not valid_odd_size(size):
        raise ValueError(f"Invalid kernel size given, make sure the size (width, height) are both positive and odd,"
                         f" size given {size}")
    kernel = np.zeros(size, dtype=np.uint8)
    kernel[int((size[0] - 1) / 2),] = 1
    return kernel


def vertical_line_kernel(size):
    r"""
    Returns a vertical line (a vertical line of ones) kernel for morphological functions
    Example of a (5,5) vertical line:

    | \| 0 0 1 0 0 \|
    | \| 0 0 1 0 0 \|
    | \| 0 0 1 0 0 \|
    | \| 0 0 1 0 0 \|
    | \| 0 0 1 0 0 \|

    :param size: a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the kernel
    """
    if not valid_odd_size(size):
        raise ValueError(f"Invalid kernel size given, make sure the size (width, height) are both positive and odd,"
                         f" size given {size}")
    kernel = np.zeros(size, dtype=np.uint8)
    kernel[:, int((size[1] - 1) / 2)] = 1
    return kernel


def sharpening_kernel(size):
    """
    Creates a sharpening kernel for image shar

    """
    if not valid_odd_size(size):
        raise ValueError(f"Invalid kernel size given, make sure the size (width, height) are both positive and odd,"
                         f" size given {size}")
    kernel = np.ones(size)
    kernel *= -1
    kernel[int((size[0] - 1) / 2), int((size[1] - 1) / 2)] = kernel.size
    return kernel
