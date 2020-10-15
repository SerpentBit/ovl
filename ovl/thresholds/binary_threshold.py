from typing import Union

import cv2
import enum

import numpy as np

from .threshold import Threshold


class BinaryThresholdType(enum.IntEnum):
    Binary = cv2.THRESH_BINARY
    BinaryInverted = cv2.THRESH_BINARY_INV
    Truncate = cv2.THRESH_TRUNC
    ToZero = cv2.THRESH_TOZERO
    ToZeroInverted = cv2.THRESH_TOZERO_INV


def is_valid_threshold_type(threshold_type):
    for current_threshold_type in BinaryThresholdType.__members__.values():
        current_type_value = current_threshold_type.value
        if threshold_type == current_type_value or threshold_type == current_type_value + cv2.THRESH_OTSU:
            return True
    return False


class BinaryThreshold(Threshold):
    """
    Creates binary image (masks) from greyscale images (black and white images)
    The basic Binary Thresholding turns all pixels that are greater or equal to the threshold parameter
    and smaller or equal to the parameter upper_bound

    For more information about the algorithms used:
    https://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
    """

    def __init__(self, threshold: int = None, upper_bound: int = None,
                 threshold_type: Union[BinaryThresholdType, int] = BinaryThresholdType.Binary,
                 otsu=False):
        """


        :param threshold: minimum value that is defined to pass the threshold
        :param upper_bound: maximum
        :param threshold_type: what to do with pixels are determined to pass the threshold,
        
        :param otsu: when true uses otsu binarization (Bi-modal thresholding),
        when using otsu binarization threshold and upper_bound are *ignored* and are not used
        """
        self.threshold_type = threshold_type
        self.threshold = threshold
        self.upper_bound = upper_bound
        self.otsu = otsu

    def convert(self, image: np.ndarray) -> np.ndarray:
        """
        Converts a greyscale image to a binary image using Binary thresholding.
        :param image: an opened image (numpy ndarray)
        :return:
        """
        return cv2.threshold(image, self.threshold, self.upper_bound, self.threshold_type)

    def validate(self, *args, **kwargs) -> bool:
        """
        Validates that the parameters for the Threshold are valid

        :param args:
        :param kwargs:
        :return:
        """
        return 0 <= self.threshold <= self.upper_bound <= 255 and is_valid_threshold_type(self.threshold_type)
