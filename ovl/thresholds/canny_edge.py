import cv2
import json
import numpy as np

from ..helpers_.remove_none_values import remove_none_values
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
        return 255 > self.high > self.low > 0

    def canny_parameters(self):
        """
        Returns the parameters of the Canny threshold that are not None
        """
        parameters = {"apertureSize": self.aperture_size,
                      "L2gradient": self.l2_gradient}
        return remove_none_values(parameters)

    def convert(self, image: np.ndarray) -> np.ndarray:
        return cv2.Canny(image, self.low, self.high, **self.canny_parameters())

    def serialize(self):
        """
        Serializes the Canny Threshold to a json string
        """
        return json.dumps({"low": self.low,
                           "high": self.high,
                           "aperture_size": self.aperture_size,
                           "l2_gradient": self.l2_gradient})

    @staticmethod
    def deserialize_canny_threshold(serialized_canny_threshold: str):
        canny_dictionary = json.loads(serialized_canny_threshold)
        return CannyEdgeThreshold(**canny_dictionary)
