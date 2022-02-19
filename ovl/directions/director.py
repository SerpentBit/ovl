import math
from logging import getLogger
from typing import *

import numpy as np

from ..exceptions.exceptions import NotEnoughTargets
from .target_selector import validate_target_selector
from ..direction_modifiers.direction_modifier import DirectionModifier

DEFAULT_DIRECTOR_LOGGER = "Director"


class Director:
    """
    Directors are object that extract usable information from the objects that were detected image.
    This information be where they are located in the image relative to the center (directions for a robot),
    how many objects were detected, identifying an object or any other logical usage of the object detection
    rather than raw image processing or computer vision.
    This is the final step before sending/using the data.

    Director.direct works in the following way:
    - if the amount of targets is less than target amount then set directions to failed_detection
    - else it passes only target_selector of targets to the direction function
    - The final result (direction function or failed_detection) is passed to the direction monitors
    - each modify_directions is applied to the result and its result is passed to the next one
    - then the final result is returned
    """

    def __init__(self, directing_function: Callable, failed_detection: Any = None, target_selector: int = 0,
                 direction_modifiers: List[DirectionModifier] = None, logger: str = None):
        """
        :param directing_function: the function that performs the initial direction calculation
        :param failed_detection: The value returned on a failed detection
        :param target_selector: selects targets after the targets have been filtered by the target filters,
        can be a number, range or selecting function
        (selecting functions receive the targets and should return False for if it failed to select)
        :param direction_modifiers: list of DirectionMonitor objects that alter the directions to be sent
        """
        self.directions = directing_function
        self.target_selector = validate_target_selector(target_selector)
        self.direction_monitors = direction_modifiers
        self.failed_detection = failed_detection
        self.logger = getLogger(logger or DEFAULT_DIRECTOR_LOGGER)

    def _inf_select(self, targets: List, selector):
        if math.isinf(selector):
            selector = None
        return targets[:selector]

    def _limit_selector(self, targets: List):
        if len(targets) < self.target_selector:
            raise NotEnoughTargets()
        return self._inf_select(targets, self.target_selector)

    def _range_selector(self, targets: List):
        low_bound, high_bound = self.target_selector
        target_amount = len(targets)
        if target_amount < low_bound:
            raise NotEnoughTargets()
        return targets[:high_bound]

    def _function_selector(self, targets: List):
        return self.target_selector(targets)

    def _select(self, targets):
        if isinstance(self.target_selector, int) or math.isinf(self.target_selector):
            return self._limit_selector(targets)
        elif isinstance(self.target_selector, tuple):
            return self._range_selector(targets)
        elif isinstance(self.target_selector, Callable):
            return self._function_selector(targets)
        else:
            raise TypeError("Invalid target selector, must be an limit (int), range (tuple of 2 ints), "
                            "or a function (returns the targets or raises FailedDetection/NotEnoughTargets)")

    def select_targets(self, targets):
        return self._select(targets)

    def direct(self, targets, image: np.ndarray) -> Any:
        """
        Returns the directions using the `vision.director` for the given targets using the image.

        `Director.direct` works in the following way:
            - if the amount of targets is less than target amount then set directions to failed_detection
            - else it passes only target_selector of targets to the direction function
            - The final result (direction function or failed_detection) is passed to the direction monitors
            - each modify_directions is applied to the result and its result is passed to the next one
            - then the final result is returned

        :param targets: the list of object that were detected in your image
        :param image: the image from which the targets were taken
        :return: Depends on the directing function and the direction monitors,
                 usually a number or tuple
        """
        try:
            targets = self.select_targets(targets)
            directions = self.directions(targets, image)
            return self.apply_direction_monitors(directions, targets, image)
        except NotEnoughTargets:
            self.logger.debug("Not enough targets to direct")
            return self.failed_detection

    def apply_direction_monitors(self, directions: Any, targets: List[np.ndarray], image: np.ndarray) -> Any:
        """
        Applies the list of direction monitors one after the other

        Direction monitors are functions that receive directions targets image and camera settings
        and change it some way, like applying a PID feedback loop, returning a "stop" value based on some condition
        (like getting close enough to the target)

        :param directions: the raw directions returned from the directions function
        :param targets: the list of targets that passed all filters
        :param image: the image from which the targets were found
        :return: the final direction result
        """
        if self.direction_monitors:
            for direction_monitor in self.direction_monitors:
                directions = direction_monitor.modify_directions(directions, targets, image)
                if direction_monitor.priority:
                    return directions
        return directions
