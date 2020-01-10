# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
import numpy as np
import copy
import cv2
from typing import *

from ..threshold import Threshold

BaseForColor = NewType("BaseForColor", Union[int, Tuple[Tuple[int, int, int], Tuple[int, int, int]]])
SERIALIZED_COLOR_KEYS = {"high", "low"}


def validate(value, ceiling):
    """
     Checks if val is positive and less than the ceiling value.
    :param value: The value to be checked (usually an int)
    :param ceiling: The highest value "val" can be. (usually an int)
    :return: True if val is less than ceiling and not negative
    """
    value = int(value)
    return 0 <= value < ceiling


def assert_hsv(hsv_point):
    """
     Makes sure the hsv point(or vector) given in the parameter has valid values.
    :param hsv_point: a 3 length list with 3 ints describing a point the hsv color space
    that describe a color limit in a range for a findContour function.
    :return: True if valid False if not.
    :rtype: bool
    """

    return validate(hsv_point[0], 180) and validate(hsv_point[1], 256) and validate(hsv_point[2], 256)


class Color(Threshold):
    def validate(self, *args, **kwargs):
        return assert_hsv(self.low_bound) and assert_hsv(self.high_bound)

    def __init__(self, low: BaseForColor, high: BaseForColor):
        """
         Constructor for the Color class
        :param high: high hsv limit of the color
        :param low: low hsv limit of the color
        """

        if type(low) is tuple:
            low = list(low)
        if type(low) is int:
            low = [low, 100, 100]
        if type(high) is tuple:
            high = list(high)
        if type(high) is int:
            high = [high, 255, 255]
        self.__low_bound = np.array(low)
        self.__high_bound = np.array(high)

    def threshold(self, image: np.ndarray) -> np.ndarray:
        return cv2.inRange(image, self.low, self.high)

    def convert(self, image: np.ndarray) -> np.ndarray:
        """
         converts a given image to hsv and then thresholds and returns the binary mask
        :param image: a BGR image
        :return: binary mask
        :rtype: numpy array
        """
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return self.threshold(hsv_image)

    def __repr__(self):
        return 'Color({}, {})'.format(repr(self.low_bound), repr(self.high_bound))

    def copy(self):
        """
        Duplicates the Color object so that changes do not affect the original color
        Useful for modifying BuiltInColors without changing the default
        :return: a copy of the color object
        """
        return copy.deepcopy(self)

    @property
    def low_bound(self):
        if isinstance(self.__low_bound, np.ndarray):
            return self.__low_bound.tolist()
        return self.__low_bound

    @property
    def high_bound(self):
        if isinstance(self.__high_bound, np.ndarray):
            return self.__high_bound.tolist()
        return self.__high_bound

    @property
    def low(self):
        """
         Returns the low hsv limit of the color.
        :return: An uint8 numpy array with the low limit of the color.
        :rtype: uint8 numpy array
        """
        return self.__low_bound

    @property
    def high(self):
        """
         Returns the high hsv limit of the color.
        :return: An uint8 numpy array with the high limit of the color.
        :rtype: uint8 numpy array
        """
        return self.__high_bound

    def __str__(self):
        return self.__repr__()
