from functools import reduce
from typing import List

import cv2
import numpy as np

from .detector import Detector
from ..partials.filter_applier import apply
from ..thresholds.threshold import Threshold


class ThresholdDetector(Detector):
    """
    ThresholdDetector is a detector used to find contours in a binary image.
    The binary image is created using a Threshold object.
    Examples of this are binary threshold, color, multicolor thresholds.


    For more information on binary thresholding and color thresholding refer to
    the documentation of the relevant Threshold object and:
    Binary Thresholding - https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
    Color Thresholding - https://docs.opencv.org/master/da/d97/tutorial_threshold_inRange.html


    Threshold also allows the usage of morphological functions
    which are functions that are applied on the binary image created by the threshold.

    .. note::

        Morphological functions are functions decorated with @image_filter that act on binary images.

    Examples for morphological functions are erosion or dilation.


    For more information on morphological functions:
    https://docs.opencv.org/3.4/d9/d61/tutorial_py_morphological_ops.html
    """

    def __init__(self, threshold: Threshold = None, morphological_functions=()):
        """
        :param threshold: a Threshold object used to create binary images
        :param morphological_functions: a list of morphological functions
        """
        self.morphological_functions = morphological_functions
        self.threshold = threshold

    def apply_threshold(self, image: np.ndarray, threshold=None) -> np.ndarray:
        """
        Gets a mask (binary image) for a given image and `Threshold` object
        (uses `self.threshold` if given threshold was none)

        :param image: the numpy array of the image
        :param threshold: the `Threshold` used to create the binary mask
        :return: the binary mask

        """
        threshold = threshold or self.threshold
        return threshold.threshold(image)

    def find_contours_in_mask(self, mask: np.ndarray, return_hierarchy=False, apply_morphs=True) -> List[np.ndarray]:
        """
        This function is used to find and extract contours (object shapes) from a binary image
        (image passed through a threshold)

        :param mask: binary image (mask), a numpy array
        :param return_hierarchy: if the hierarchy should be returned
        :param apply_morphs: if the morphological functions should be applied.
        :return: the list of contours
        """
        mask = self.apply_morphological_functions(mask) if apply_morphs else mask
        result = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(result) == 3:
            _, contours, hierarchy = result
        elif len(result) == 2:
            contours, hierarchy = result
        else:
            raise ValueError("Invalid output from cv2.findContours, check that your cv2 (OpenCV) version is supported")
        return (contours, hierarchy) if return_hierarchy else contours

    def detect(self, image: np.ndarray, return_hierarchy=False, *args, **kwargs) -> List[np.ndarray]:
        """
        Gets a list of all the contours within the threshold that was given

        :param image: image from which to get the contours
        :param return_hierarchy: if the hierarchy should be returned
        :return: list of all contours matching the range of hsv colours

        """
        image_mask = self.apply_threshold(image)
        return self.find_contours_in_mask(image_mask, return_hierarchy=return_hierarchy)

    def apply_morphological_functions(self, mask, morphological_functions=None):
        """
        Applies all morphological functions on the mask (binary images) created using the threshold,
        Morphological functions are functions that are applied
        to binary images to alter the shape of "detected" regions


        :param mask: the mask on which the functions should be applied
        :param morphological_functions: list of morphological_functions to be
         applied instead of self.morphological_functions
        :return: the applied mask
        """
        if type(self.morphological_functions) not in (tuple, list, set):
            return mask
        morphological_functions = morphological_functions or self.morphological_functions
        return reduce(apply, morphological_functions, mask)

    def __repr__(self):
        return f"<ThresholdDetector {self.threshold}>"

    def serialize(self):
        return {
            "threshold": self.threshold.serialize(),
            "morphological_functions": [m.serialize() for m in self.morphological_functions]
        }

    @classmethod
    def deserialize(cls, data):
        return cls(morphological_functions=data["morphological_functions"],
                   threshold=data["threshold"])
