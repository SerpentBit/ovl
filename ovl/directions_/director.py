from typing import Callable, List, Any
import math

from .direction_monitors.direction_monitor import *
from ..camera_.camera_settings import *


class Director:
    """
    An object responsible of extrapolating directions from the detection of a Vision object
    This is the final step before sending/using the data.
    A director is built from a directing function and directing monitor
    """
    def __init__(self, directing_function: Callable, failed_detection: Any, target_amount: int = 1,
                 direction_monitors: List[DirectionMonitor] = None):
        """

        :param directing_function: the function that performs the initial direction calculation
        :param failed_detection: The value returned on a failed detection
        :param target_amount: the target amount to find, if the value is 0
                              the target amount (minimum amount) removed and is infinite
        :param direction_monitors: list of DirectionMonitor objects that alter the directions to be sent
        """
        self.directions = directing_function
        if not isinstance(target_amount, int):
            raise ValueError("Target amount must be an integer, got {} of type {}.".format(target_amount,
                                                                                           type(target_amount)))
        self.target_amount = target_amount if target_amount != 0 else math.inf
        self.direction_monitors = direction_monitors
        self.failed_detection = failed_detection

    def direct(self, contours: List[np.ndarray], image: np.ndarray, camera_settings, sorter=None) -> Any:
        """
        Returns the director for the given contours
        :param contours: the list of contours (numpy ndarrays) from which to extrapolate target direction
        :param image: the image from which the contours were taken
        :param camera_settings: The Camera settings, including position and calibration
        :param sorter: A sorter function to be applied on the contours, or None to not apply one
        :return: Depends on the directing function and the direction monitors,
                 usually a number or a string
        """
        if not len(contours) >= self.target_amount:
            directions = self.failed_detection
        else:
            if sorter is not None:
                contours = sorter(contours)
            if math.isfinite(self.target_amount):
                contours = contours[:self.target_amount]
            directions = self.directions(contours, image)

        return self.apply_direction_monitors(directions, contours, image, camera_settings)

    def apply_direction_monitors(self, directions: Any, contours: List[np.ndarray],
                                 image: np.ndarray, camera_settings: CameraSettings) -> Any:
        """
        Applies the list of direction monitors one after the other
        :param directions: the raw directions returned from the directions function
        :param contours: the list of contours that passed all filters
        :param image: the image from which the contours were found
        :param camera_settings: settings related to the camera, like position or calibration
        :return: the final direction result
        """
        if self.direction_monitors:
            for direction_monitor in self.direction_monitors:
                directions = direction_monitor.monitor(directions, contours, image, camera_settings)
                if direction_monitor.priority:
                    return directions
        return directions
