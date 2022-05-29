import types
from typing import List

import numpy as np

from . import vision
from ..detectors.detector import Detector


class AmbientVision:
    """
    A mesh of 2 vision objects that extends one of the visions at a time.

    The visions are swapped every main_amount of update_vision calls.
    This makes the "ambient_vision" run in the background once every multiple frames.

    The example includes only general instructions, 2 vision objects need to be defined to detect something

    An example will be as follows:

    .. code-block:: python

        vision1 = Vision(....)

        vision2 = Vision(....)

        vision_controller = AmbientVision(main_vision=vision1, ambient_vision=vision2, main_amount=3)

        while True:
            image = vision_controller.get_image()

            targets, image = vision_controller.detect(image)

            vision_controller.update_vision()


    you can get the current vision object using vision_controller.current_vision


    """

    def __init__(self, main_vision: vision.Vision, ambient_vision: vision.Vision,
                 main_amount: int, start_ambient: bool = False):
        self.main_vision = main_vision
        self.ambient_vision = ambient_vision
        self.main_amount = main_amount
        self.is_ambient = start_ambient
        if start_ambient:
            self.counter = 0
            self.current_vision = main_vision
        else:
            self.counter = main_amount
            self.current_vision = ambient_vision

    @property
    def detector(self) -> Detector:
        return self.current_vision.detector

    @property
    def image_filters(self) -> List[types.FunctionType]:
        return self.current_vision.image_filters

    @property
    def directions(self):
        return self.current_vision.director

    @property
    def director(self):
        return self.current_vision.director

    def get_image(self) -> np.ndarray:
        """
        Take a picture using the current vision

        See `Vision.get_image` for more information
        """
        return self.current_vision.get_image()

    def apply_image_filters(self, image: np.ndarray) -> np.ndarray:
        """
        Applies all the image filters of the current vision on the given image

        See `Vision.apply_image_filters` for more information
        """
        return self.current_vision.apply_image_filters(image)

    def detect(self, image: np.ndarray, verbose=False, *args, **kwargs):
        """
        Gets targets and applies all filters and returns the result,
        thus detecting the object according to the specifications in the vision,
        Uses the current vision

        :param image: image in which the vision should detect an object
        :param verbose: if true prints additional information about contour filtering
        :return: targets, ratio list (from the filter functions) and the filtered image
        """
        return self.current_vision.detect(image, verbose=verbose, *args, **kwargs)

    def get_directions(self, targets, image):
        """
        Returns the directions for the given image and contours using the current vision

        :param targets: the final contours detected.
        :param image: the image where the contours were detected in.
        :return: the directions
        """
        return self.current_vision.get_directions(targets, image)

    def update_vision(self):
        """
        Increases the inner counter and swaps the ambient and the main vision
        after the set number of updates (self.main_amount)

        This is used to switch between the main vision and ambient vision
        """
        if self.counter < self.main_amount:
            self.counter += 1
            self.current_vision = self.main_vision
            self.is_ambient = False
        else:
            self.counter = 0
            self.current_vision = self.ambient_vision
            self.is_ambient = True
