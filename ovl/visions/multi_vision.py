import asyncio
import functools
import logging
from typing import Union, List, Any, Generator, Dict, Tuple

from numpy import ndarray

from utils.get_function_name import get_function_name
from .ambient_vision import AmbientVision
from ..utils.constants import BASE_LOGGER, MULTIVISION_LOGGER
from ..utils.types import VisionLike

logger = logging.getLogger(f"{BASE_LOGGER}.{MULTIVISION_LOGGER}")
NO_VISIONS_GIVEN_MESSAGE = "No visions were given to the MultiVision object."


class MultiVision:
    """
    An object used to switch between multiple vision objects.
    It does this by having a list of visions and a connection and network_location to update from
    So it can be automatically updated to swap to the desired Vision object
    use the start method to start an infinite loop that returns images and detections

    .. code-block:: python

        connection = ovl.NetworkTablesConnection(1937)

        vision1 = ovl.Vision(....)
        vision2 = ovl.Vision(....)
        vision3 = ovl.Vision(....)

        controller_network_connection = ovl.NetworkLocation(table_key="current_vision")

        multi_vision = ovl.MultiVision([vision1, vision2, vision3], connection)

        for directions, targets, image  in multi_vision.start():

            # do something with the generated data

            # like sending the data or displaying the targets

            multi_vision.send(directions)

            ovl.display_contours(image, targets, delay=1)

    """

    def __init__(self, visions: Union[List[VisionLike], Dict[Any, VisionLike]], default_vision_index=None):
        self.pre_iteration_func = None
        self.post_iteration_func = None

        self.visions = visions
        if len(self.visions) == 0:
            logger.error(NO_VISIONS_GIVEN_MESSAGE)
            raise ValueError(NO_VISIONS_GIVEN_MESSAGE)

        if isinstance(visions, list):
            default_vision_index = default_vision_index or 0
            self._validate_vision_index_list(default_vision_index)
        elif isinstance(visions, dict):
            default_vision_index = default_vision_index or list(visions.keys())[0]
            self._validate_vision_index_dictionary(default_vision_index)
        self.default_vision = self.visions[default_vision_index]
        self.current_vision = self.default_vision
        self.default_vision_index = default_vision_index
        self.upcoming_vision = None
        self._update_vision_func = None
        self._update_task = None

    @property
    @functools.lru_cache
    def vision_amount(self) -> int:
        """
        Returns the amount of visions in the controller

        :return: the amount of visions
        """
        return len(self.visions)

    @property
    def is_ambient(self) -> bool:
        """
         Returns True if the current_vision vision is an Ambient vision object

        :return: if the current vision is an AmbientVision
        """
        return isinstance(self.current_vision, AmbientVision)

    def before_iteration(self, func):
        """
        Decorator that runs the function before each iteration of the MultiVision loop

        :param func: the function to run before each iteration
        """
        self.pre_iteration_func = func
        return func

    def after_iteration(self, func):
        """
        Decorator that runs the function before each iteration of the MultiVision loop

        :param func: the function to run before each iteration
        """
        self.post_iteration_func = func
        return func

    def vision_updater(self, update_vision):
        """
        This function is a decorator that can be used to set custom logic to when vision updating occurs, it will be
        called constantly, but will actually update only once a detection iteration finishes.
        """

        @functools.wraps(update_vision)
        async def _update_vision():
            logger.debug("Starting vision update task, task_id: %s", get_function_name(_update_vision))
            is_update_async = asyncio.iscoroutinefunction(update_vision)
            while True:
                current_vision = self.current_vision
                if is_update_async:
                    next_vision = await update_vision(current_vision)
                else:
                    next_vision = update_vision(current_vision)
                self.upcoming_vision = next_vision

        self._update_vision_func = _update_vision()
        return update_vision

    def stop_update_task(self):
        """
        Stops the update task if it is running
        """
        if self._update_task is not None:
            self._update_task.cancel()
        else:
            raise ValueError("No update task is running")

    def set_new_vision(self):
        self.current_vision = self.upcoming_vision or self.current_vision

    async def start(self) -> Generator[Tuple[Any, "ndarray", Any], None, None]:
        """
        Start an infinite generator that takes an image
        detects with the current vision and returns the list of targets the image and directions
        and should be used as follows:

        .. code-block:: python

            connection = ovl.NetworkTablesConnection(1937)

            vision1 = ovl.Vision(....)
            vision2 = ovl.Vision(....)
            vision3 = ovl.Vision(....)

            update_location = ovl.NetworkLocation(table_key="current_vision")

            multi_vision = ovl.MultiVision([vision1, vision2, vision3], connection, update_location)

            for directions, targets, image  in multi_vision.start():

                # do something with the generated data

                # like sending the data or displaying the targets

                multi_vision.send(directions)

                ovl.display_contours(image, targets, delay=1)

        Note: automatically updates AmbientVision's vision swapping (AmbientVision.update_vision())!

        :yields: targets, image and directions
        """
        self._update_task = asyncio.create_task(self._update_vision_func)
        while True:
            self.set_new_vision()

            if self.pre_iteration_func:
                self.pre_iteration_func()

            image = await asyncio.to_thread(self.current_vision.get_image)
            targets, filtered_image = self.current_vision.detect(image)
            directions = self.current_vision.director.direct(targets, filtered_image)
            if self.is_ambient:
                self.current_vision.update_vision()
            yield directions, targets, filtered_image

            if self.post_iteration_func:
                self.post_iteration_func()

    def _validate_vision_index_list(self, index):
        """
        Validates the index is in the list of visions

        :param index: the index to validate
        :return: the index
        """
        return 0 <= index < len(self.visions)

    def _validate_vision_index_dictionary(self, index):
        """
        Validates the index is a key of a vision in the controller

        :param index: the index to validate
        :return: the index
        """
        return index in self.visions
