# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
import cv2
import numpy as np

from .color import Color
from ..threshold import Threshold


class MultiColor(Threshold):
    """
    Multi Color is similar to the Color object, but allows multiple color ranges
    a main use is for representing the red color range.

    Example Code:

    .. code-block:: python

        orange = [[10, 100, 100], [18, 255, 255]]
        green = [[45, 100, 100], [75, 255, 255]]
        orange_and_green = MultiColor([orange, green])



    There are multiple built-in "battery included" pre-made color object
    for instant use in testing and tuning
    List of colors:
      Red (MultiColorObject) : Red (low) + Red (high)
      Red (Low): [0, 100, 100], [8, 255, 255]
      Red (High): [172, 100, 100], [179, 255, 255]
      Note: in order to find red, use both ranges (low and high) and use the sum of both results.
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

    def __init__(self, colors):
        """
        Example:
            .. code-block:: python

              MultiColor([Color([15, 50, 50], [45, 255, 125]),
                         [[105, 175, 25], [115, 255, 255]]])


         These are different ways to create ranges of colors

        :param colors: A list of Color objects or tuple that can be turned into a color object

         """
        self.colors = colors
        for index, color in enumerate(colors):
            if type(color) in (list, tuple):
                self.colors[index] = Color(*color)

    def convert(self, image: np.ndarray):
        """
        Thresholds an image using the color ranges,
        all pixels that are not in the color ranges defined are set to black (0, 0, 0)
        and all others to white (255, 255, 255)
        """
        if self.colors is None:
            raise ValueError("Cannot convert an image to a binary, no colors given.")
        if len(self.colors) == 0:
            raise ValueError("Cannot convert an image to binary, no colors given.")
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        binary_image = self.colors[0].threshold(hsv_image)
        if len(self.colors) < 1:
            return binary_image
        for color in self.colors[1:]:
            binary_image = cv2.bitwise_or(binary_image, color.threshold(hsv_image))

        return binary_image

    def validate(self, *args, **kwargs) -> bool:
        for color in self.colors:
            if type(color) not in Color:
                if not color.validate():
                    return False
        return True

    def __str__(self):
        return ', '.join([str(color) for color in self.colors])

    def __repr__(self):
        return 'MultiColor(0)'.format([repr(i) for i in self.colors])
