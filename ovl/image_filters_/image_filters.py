# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
import cv2
import numpy as np

from .image_filter import image_filter
from ..helpers_.remove_none_values import remove_none_values
from .kernels import validate_odd_size


def convert_to_hsv(img):
    """
     converts an image to hsv - Mainly for beginner use
    :param img: image to be converted
    :return: the converted image
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


@image_filter
def sharpen_image(image, size=(3, 3)):
    """
     Sharpens an image by preforming convolution it with a sharpening matrix
    :param image: the image (numpy array)
    :param size: the size of the sharpening matrix
    :return: the new sharpened image
    """

    validate_odd_size(size)
    kernel = np.ones(size)
    kernel *= -1
    kernel[int((size[0] - 1) / 2), int((size[1] - 1) / 2)] = kernel.size
    return cv2.filter2D(image, -1, kernel)


@image_filter
def adaptive_brightness(image, brightness=127, hsv=False):
    """
     Changes the brightness of every pixel so that the average is the target average
    :param image: The image to be changed (Numpy array)
    :param brightness: the target average for the image
    :type brightness: int (int between 0 - 100)
    :param hsv: bool noting if the image is in hsv
    :return: a copy of the image changed
    :rtype: numpy array
    """
    image = image if hsv else cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    brightness = brightness * 2.55
    image_hue_mean = cv2.mean(image)[2]
    increase = brightness - image_hue_mean
    vid = image[:, :, 2]
    if increase > 0:
        vid = np.where(vid + increase <= 255, vid + increase, 255)
    else:
        vid = np.where(vid + increase >= 0, vid + increase, 0)
    image[:, :, 2] = vid
    image = image if hsv else cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image


@image_filter
def change_brightness(image, change=25, hsv_image=False):
    """
     Changes the brightness of every pixel of a BGR image by the given amount
    :param image: The image to be changed (Numpy array)
    :param change: the change (integer) (The min brightness is 0 and max is 100)
    :type change: int
    :param hsv_image: bool noting if the image is in hsv
    :return: a copy of the image changed
    """
    image = image if hsv_image else cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    change = change * 2.55
    vid = image[:, :, 2]
    if change > 0:
        vid = np.where(vid + change <= 255, vid + change, 255)
    else:
        vid = np.where(vid + change >= 0, vid + change, 0)
    image[:, :, 2] = vid
    image = image if hsv_image else cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image


@image_filter
def rotate_image(image, angle=180):
    """
    Rotates an image by a given amount of degrees.
    Note that the rotated image's dimensions will most likely stay the same if the angle is not 90, -90 or 180
    :param image: the image to be rotated
    :param angle: the angle to rotate in (positive is to the left, negative to the right)
    :return: the rotated image
    """
    angle = angle % 360
    shortcut_angles = {
        90: rotate90_left,
        -90: rotate90_right,
        180: rotate180,
        -180: rotate180
    }
    if angle in shortcut_angles:
        return shortcut_angles[angle]()(image)
    elif angle == 0:
        return image
    else:
        return rotate_by_angle()(image, angle)


@image_filter
def rotate_by_angle(image, angle):
    """
    Rotates the given image by a given angle
    :param image: the image to be rotated
    :param angle: the angle of rotation
    :return: the rotated image
    """
    (height, width) = image.shape[:2]
    center_xy = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center_xy, -angle, 1.0)
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    rotated_image_dimensions = (int((height * sin) + (width * cos)), int((height * cos) + (width * sin)))
    rotation_matrix[0, 2] += (rotated_image_dimensions[0] / 2) - center_xy[0]
    rotation_matrix[1, 2] += (rotated_image_dimensions[1] / 2) - center_xy[1]
    return cv2.warpAffine(image, rotation_matrix, rotated_image_dimensions)


@image_filter
def rotate90_left(image):
    """
    Return a copy of the image rotated 90 degrees to the left (_counter-clockwise)
    :param image: numpy array, image to be rotated
    :return: a copy of the image rotated.
    """
    (height, width) = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (height, width))


@image_filter
def rotate90_right(image):
    """
    Return a copy of the image rotated 90 degrees to the right (clockwise)
    :param image: numpy array, image to be rotated
    :return:
    """
    (height, width) = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 270, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (height, width))


def rotate180(image):
    """
    Return a copy of the image rotated 180 degrees
    :param image:  numpy array, image to be rotated
    :return: a copy of the image rotated.
    """
    (height, width) = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 180, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (height, width))


@image_filter
def non_local_mean_denoising(image, h, h_color, template_window_size, search_window_size, destination=None):
    parameters = {"h": h,
                  "hColor": h_color,
                  "templateWindowSize": template_window_size,
                  "seasonWindowSize": search_window_size,
                  "dst": destination
                  }
    return cv2.fastNlMeansDenoisingColored(image,
                                           **remove_none_values(parameters))


@image_filter
def gaussian_blur(image, kernel_size=(3, 3), sigma_x=5, sigma_y=None, border_type=None):
    parameters = {"ksize": kernel_size,
                  "sigmaX": sigma_x,
                  "sigmaY": sigma_y,
                  "borderType": border_type}
    return cv2.GaussianBlur(image, **remove_none_values(parameters))


@image_filter
def crop_image(image, point, dimensions):
    """
    Crops a given rectangle from a given image
    :param image: an image (numpy array)
    :param point: (x, y) coordinates that is the top left corner of the rectangle
    :param dimensions: (width, height) of the rectangle
    :return: the region of the image
    """
    x, y = point
    width, height = dimensions
    return image[x: x + width, y: y + height]
