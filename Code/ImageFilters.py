# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
import cv2
import numpy as np


def validate_odd_size(size):
    """
    Action: validates that a kernel shape is of odd  ints and of size 2
    :param size: the shape (size) to be checked
    :return: doesnt raise an error if it's ok.
    """
    if type(size) not in (list, tuple):
        raise TypeError("Kernel size must be a tuple or list of 2 odd integers!")
    if len(size) != 2:
        raise ValueError("Kernel size must be a tuple or list of 2 odd integers!")
    if size[0] % 2 != 1 or size[1] % 2 != 1:
        raise ValueError("Kernel size must be 2 odd integers!")


def is_odd_size(size):
    """
    Action: validates that a kernel shape is of odd  ints and of size 2
    :param size: the shape (size) to be checked
    :return: doesnt raise an error if it's ok.
    """
    if type(size) not in (list, tuple):
        return False
    if len(size) != 2:
        return False
    if size[0] % 2 != 1 or size[1] % 2 != 1:
        return False
    return True


def validate_kernel(size):
    """
    Action: Validates the Size of a kernel
    :param size: the size (shape)
    :return:
    """
    if type(size) not in (list, tuple):
        raise TypeError("Kernel size must be a tuple or list!")
    if len(size) != 2:
        raise ValueError("Kernel size must be a tuple or list!")
    for i in size:
        if type(i) is not int:
            raise TypeError("Size must consist only of ints")


def cross_kernel(size):
    """
    Action: Returns a cross (ones in a cross) kernel for morphological functions
    Example of a (5,5) cross:
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    | 1 1 1 1 1 |
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    :param size:  a tuple of size 2 of 2 odd integers denoting the size of the kernel
    :return: the numpy.array of the cross shape
    """
    validate_odd_size(size)
    return cv2.getStructuringElement(cv2.MORPH_CROSS, ksize=size)


def rectangle_kernel(size):
    """
    Action: Returns a rectangle (all ones) kernel for morphological functions
    Example of a (5,5) rectangle:
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    :param size:  a tuple of size 2 of 2 odd integers denoting the size of the kernel
    :return: the numpy.array of the cross shape
    """
    return cv2.getStructuringElement(cv2.MORPH_RECT, ksize=size)


def ellipse_kernel(size):
    """
    Action: Returns an ellipse (ones in the shape of an ellipse) kernel for morphological functions
    Example of a (5,5) ellipse:
    | 0 0 1 0 0 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 0 0 1 0 0 |
    :param size: a tuple of size 2 of 2 odd integers denoting the size of the kernel
    :return:
    """
    validate_odd_size(size)
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=size)


def horizontal_line_kernel(size):
    """
    Action: Returns an horizontal line (a horizontal line of ones) kernel for morphological functions
    Example of a (5,5) horizontal line:
    | 0 0 0 0 0 |
    | 0 0 0 0 0 |
    | 1 1 1 1 1 |
    | 0 0 0 0 0 |
    | 0 0 0 0 0 |
    :param size: a tuple of size 2 of 2 odd integers denoting the size of the kernel
    :return:
    """
    validate_odd_size(size)
    arr = np.zeros(size, dtype=np.uint8)
    arr[int((size[0] - 1) / 2), ] = 1
    return arr


def vertical_line_kernel(size):
    """
    Action: Returns a vertical line (a vertical line of ones) kernel for morphological functions
    Example of a (5,5) vertical line:
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |

    :param size:  a tuple of size 2 of 2 odd integers denoting the size of the kernel
    :return:
    """
    validate_odd_size(size)
    arr = np.zeros(size, dtype=np.uint8)
    arr[:, int((size[1] - 1) / 2)] = 1
    return arr


def convert_to_hsv(img):
    """
    Action: converts an image to hsv - Mainly for beginner use
    :param img: image to be converted
    :return: the converted image
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def sharpen_image(image, size=(3, 3)):
    validate_odd_size(size)
    kernel = np.ones(size)
    kernel *= -1
    kernel[int((size[0] - 1) / 2), int((size[1] - 1) / 2)] = kernel.size
    return cv2.filter2D(image, -1, kernel)


def adaptive_brightness(src, target_average=127, img_in_hsv=False):
    """
    Action: Changes the brightness of every pixel so that the average is the target average
    :param src: The image to be changed (Numpy array)
    :param target_average: the target average for the image
    :type target_average: int (int between 0 - 255)
    :param img_in_hsv: bool noting if the image is in hsv
    :return: a copy of the image changed
    """
    src = src.copy()
    if not img_in_hsv:
        src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    increase = cv2.mean(src)[2] - target_average
    vid = src[:, :, 2]
    vid = np.where(vid <= 255 - increase, vid + increase, 255)
    src[:, :, 2] = vid
    if not img_in_hsv:
        src = cv2.cvtColor(src, cv2.COLOR_HSV2BGR)
    return src


def change_brightness(src, change=20,  img_in_hsv=False):
    """
    Action: Changes the brightness of every pixel by the given amount
    :param src: The image to be changed (Numpy array)
    :param change: the change (integer)
    :type change: int
    :param img_in_hsv: bool noting if the image is in hsv
    :return: a copy of the image changed
    """
    src = src.copy()
    if not img_in_hsv:
        src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    vid = src[:, :, 2]
    vid = np.where(vid <= 255 - change, vid + change, 255)
    src[:, :, 2] = vid
    if not img_in_hsv:
        src = cv2.cvtColor(src, cv2.COLOR_HSV2BGR)
    return src


def rotate_by_angle(image, angle):
    """
    Action: rotates the given image by a given angle
    :param image:
    :param angle:
    :return:
    """
    (h, w) = image.shape[:2]
    center_xy = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center_xy, -angle, 1.0)
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_image_dimensions = (int((h * sin) + (w * cos)), int((h * cos) + (w * sin)))
    rotation_matrix[0, 2] += (new_image_dimensions[0] / 2) - center_xy[0]
    rotation_matrix[1, 2] += (new_image_dimensions[1] / 2) - center_xy[1]
    return cv2.warpAffine(image, rotation_matrix, new_image_dimensions)


def rotate90_left(image):
    """
    Action: return a copy of the image rotated 90 degrees to the left (counter-clockwise)
    :param image: numpy array, image to be rotated
    :return: a copy of the image rotated.
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (h, w))


def rotate90_right(image):
    """
    Action: return a copy of the image rotated 90 degrees to the right (clockwise)
    :param image: numpy array, image to be rotated
    :return:
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 270, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (h, w))


def rotate180(image):
    """
    Action: return a copy of the image rotated 180
    :param image:  numpy array, image to be rotated
    :return: a copy of the image rotated.
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 180, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (h, w))
