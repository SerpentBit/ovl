# Copyright 2018 Ori Ben-Moshe - All rights reserved.
import cv2
import numpy as np


def convert_to_hsv(img):
    """
    Action: converts an image to hsv - Mainly for beginner use
    :param img: image to be converted
    :return: the converted image
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


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
