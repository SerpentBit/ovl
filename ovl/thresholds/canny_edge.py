import json

import cv2
import numpy as np

from .threshold import Threshold


class CannyEdge(Threshold):
    """
    A Canny edge detection Threshold
    Creates a binary image using the Canny edge detection algorithm
    See:
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
    """

    def __init__(self, low: int, high: int, aperture_size: int = None, l2_gradient: bool = None):
        self.low = low
        self.high = high
        self.aperture_size = aperture_size
        self.l2_gradient = l2_gradient

    def validate(self) -> bool:
        """
        Validate that the Canny edge parameters are valid
        """
        return 255 > self.high >= self.low > 0

    def threshold(self, image: np.ndarray) -> np.ndarray:
        return cv2.Canny(image, self.low, self.high, apertureSize=self.aperture_size,
                         L2gradient=self.l2_gradient)

    def serialize(self):
        """
        Serialize the Canny edge parameters
        """
        return {
            'low': self.low,
            'high': self.high,
            'aperture_size': self.aperture_size,
            'l2_gradient': self.l2_gradient
        }

    @staticmethod
    def deserialize_canny_threshold(serialized_canny_threshold: str):
        return

    def __repr__(self):
        return f"CannyEdge(low={self.low}, high={self.high}," \
               f" aperture_size={self.aperture_size}, l2_gradient={self.l2_gradient})"

    def __str__(self):
        return repr(self)

    @classmethod
    def deserialize(cls, data):
        return cls(**data)
