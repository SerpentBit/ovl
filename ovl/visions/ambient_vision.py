import numpy as np
from typing import List, Tuple
import types

from . import vision
from ..connections import connection
from ..thresholds.threshold import Threshold


class AmbientVision:
    """
    A Mash of 2 vision objects that extends one of the visions at a time.
    The visions are swapped every main_amount of update_vision calls.
    This makes the "ambient_vision" run in the background once every multiple frames.

    An example will be as follows:
    vision1 = Vision(....)
    vision2 = Vision(....)

    vision_controller = AmbientVision(main_vision=vision1, ambient_vision=vision2, main_amount=3)

    while True:
        image = vision_controller.get_image()
        contours, image = vision_controller.detect(image)
    """

    def __init__(self, main_vision: vision.Vision, ambient_vision: vision.Vision,
                 main_amount: int, start_ambient: bool = False):
        self._main_vision = main_vision
        self._ambient_vision = ambient_vision
        self.main_amount = main_amount
        self._is_ambient = start_ambient
        if start_ambient:
            self._counter = 0
            self._current_vision = main_vision
        else:
            self._counter = main_amount
            self._current_vision = ambient_vision

    @property
    def main_vision(self) -> vision.Vision:
        return self.main_vision

    @property
    def ambient_vision(self) -> vision.Vision:
        return self.ambient_vision

    @property
    def connection(self) -> connection.Connection:
        return self._current_vision.connection

    @property
    def threshold(self) -> Threshold:
        return self._current_vision.threshold

    @property
    def image_filters(self) -> List[types.FunctionType]:
        return self._current_vision.image_filters

    @property
    def directions(self):
        return self._current_vision.director

    def is_ambient(self) -> bool:
        """
        Returns true if the current vision is the ambient one
        """
        return self._is_ambient

    def get_image(self) -> np.ndarray:
        """
         Take a picture using the current vision
        """
        return self._current_vision.get_image()

    def get_filtered_image(self) -> np.ndarray:
        """
         Returns the image from the current vision with
                all of the image filters applied on it.
        :return: the filtered image
        :rtype: ndarray
        """
        return self._current_vision.get_filtered_image()

    def apply_image_filters(self, image: np.ndarray) -> np.ndarray:
        """
        Applies all of the image filter of the current vision on the given image
        """
        return self._current_vision.apply_image_filters(image)

    def apply_morphological_functions(self, mask: np.ndarray) -> np.ndarray:
        """
        Applies the current vision's morphological functions on
        a binary mask (numpy ndarray)
        See Vision.apply_morphological_functions for full description
        """
        return self._current_vision.apply_morphological_functions(mask)

    def find_contours_in_mask(self, mask: np.ndarray, save: bool = True,
                              return_hierarchy: bool = False) -> List[np.ndarray]:
        """
        Returns a list of contours from a given binary mask (numpy ndarray),
        using the current vision
        See Vision.find_contours_in_mask for full description
        """
        return self._current_vision.find_contours_in_mask(mask, save, return_hierarchy)

    def find_contours(self, image: np.ndarray, threshold=None, return_hierarchy=False) -> List[np.ndarray]:
        """
        Find contours in the given image, using the current vision.
        See Vision.find_contours for full description
        """
        return self._current_vision.find_contours(image, threshold, return_hierarchy)

    def detect(self, image: np.ndarray, verbose=False
               ) -> Tuple[List[np.ndarray], np.ndarray]:
        """
        Gets contours and applies all filters and returns the result,
        thus detecting the object according to the specifications in the vision,
        Uses the current vision
        :param image: image in which the vision should detect an object
        :param verbose: if true prints additional information about contour filtering
        :return: contours, ratio list (from the filter functions) and the filtered image
        """
        return self._current_vision.detect(image, verbose=verbose)

    def send(self, data, *args, **kwargs):
        """
        Sends a given value to the current vision's connection object
        :param data: the data to be sent
        :param args: any other parameters to the specific connection object
        :param kwargs:
        :return: Whatever the underlying connection object returns, usually the parameter data
        """
        return self._current_vision.send(data, *args, **kwargs)

    def get_directions(self, contours, image, sorter=None):
        """
        Returns the directions for the given image and contours using the current vision
        :param contours: the final contours detected.
        :param image: the image where the contours were detected in.
        :param sorter: a sorter function that can be added to be applied before getting directions
        :return: the directions
        """
        return self._current_vision.get_directions(contours, image, sorter)

    def update_vision(self):
        """
        Increases the inner counter and swaps the ambient and the main vision
        after the set number of updates (self.main_amount)
        """
        if self._counter < self.main_amount:
            self._counter += 1
            self._current_vision = self.main_vision
            self._is_ambient = False
        else:
            self._counter = 0
            self._current_vision = self.ambient_vision
            self._is_ambient = True
