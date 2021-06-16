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
    """
    Color is a Threshold object (an object that turns an image to a binary image
    - an image with pixels with the value 1 and 0)
    Color object thresholds using 2 HSV color ranges.

    Read more about HSV here:
    https://www.lifewire.com/what-is-hsv-in-design-1078068

    HSV Ranges in OVL (And in the underlying open-cv (cv2)) are:
    Hue - 0 to 179 (360/2 so divide any regular HSV value you use by 2)

        So if Yellow is 40 - 80 (degrees) in regular HSV palette its 20 to 40 in ovl
    Saturation - 0 to 255 (255 is equal to 1 or 100%)
    Value - 0 to 255 (255 is equal to 1 or 100%)

    2 ranges are passed to the Constructor:
        1) Low HSV Range - the lowest acceptable H S V values ([low_H, low_S, low_V])
        2) High HSV Range - the highest acceptable H S V values ([high_H, high_S, high_V])

    .. code-block:: python

        low_range = [15, 100, 100]
        high_range = [45, 255, 255]
        color = ovl.Color(low_range, high_range)



    The color object can the be passed to a Vision object to threshold binary images
    Threshold object can be used by themselves using the color.convert() method.

    NOTE: Threshold objects automatically convert images to HSV (From the default BGR)

    There are multiple built in "battery included" pre-made color object
    for instant use in testing and tuning
    List of colors:
      Red (MultiColorObject) : Red (low) + Red (high)
      Red (Low): [0, 100, 100], [8, 255, 255]
      Red (High): [172, 100, 100], [179, 255, 255]
      Note: in order to find red, use both ranges (low and high) and use the some of both results.
      Blue: [105, 100, 100], [135, 255, 255]
      Green: [45, 100, 100], [75, 255, 255]
      Yellow: [20, 100, 100], [55, 255, 255]
      Orange: [10, 100, 100], [18, 255, 255]
      Grey: [0, 0, 0], [179, 50, 195]
      Black: [0, 0, 0], [179, 255, 30]
      White: [0, 0, 200], [179, 20, 255]
      Teal: [110, 100, 100], [130, 255, 255]
      Purple: [135, 100, 100], [165, 255, 255]
    """

    def __init__(self, low: BaseForColor, high: BaseForColor):
        """
         Constructor for the Color used to turn images to binary images based on
         HSV color space (pixels that are in the specified HSV Range)
         H - 0 - 179
         S - 0 - 255
         V - 0 - 255

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

    def validate(self, *args, **kwargs):
        return assert_hsv(self.low_bound) and assert_hsv(self.high_bound)

    def threshold(self, image: np.ndarray) -> np.ndarray:
        return cv2.inRange(image, self.low, self.high)

    def convert(self, image: np.ndarray) -> np.ndarray:
        """
        Converts a given image to hsv and then thresholds and returns the binary mask

        :param image: a BGR image
        :return: binary mask
        :rtype: numpy array
        """
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return self.threshold(hsv_image)

    def __repr__(self):
        return f'Color({repr(self.low_bound)}, {repr(self.high_bound)})'

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
