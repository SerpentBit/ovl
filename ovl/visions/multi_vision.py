import numpy as np
from typing import Union, List, Any, Generator, Tuple

from .vision import Vision
from .ambient_vision import AmbientVision
from ..connections.connection import *
from ..connections.network_location import NetworkLocation


class MultiVision:
    """
    An object used to switch between multiple vision objects.
    It does this by having a list of visions and a connection and network_location to update from
    So it can be automatically updated to swap to the desired Vision object
    use the start method to start an infinite loop that returns images and detections

        for contours, image, directions in multi_vision.start():
            # do something with the generated data
            # like sending the data or displaying the contours
            multi_vision.send(directions)
            ovl.display_contours(image)
    """
    def __init__(self, vision_list: List[Union[Vision, AmbientVision, Any]], update_connection: Connection,
                 update_location: Union[NetworkLocation, None] = None, default_vision=0):
        self.current = vision_list[default_vision]
        self.index = default_vision
        self.vision_list = vision_list
        self.connection = update_connection
        self.update_location = update_location

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def is_ambient(self) -> bool:
        """
         Returns True if the current_vision vision is an Ambient vision object
        :return:
        """
        return isinstance(self.current, AmbientVision)

    def send(self, data, *args, **kwargs) -> Any:
        """
        Sends the value to the target destination of the current_vision vision object
        :param data: the data to be sent
        :return:
        """
        return self.current.send(data=data, *args, **kwargs)

    def switch_vision(self, index: int) -> None:
        """
        Switches the current vision to the one given
        """
        self.index = int(index)
        if index > len(self.vision_list) or index < 0:
            return
        self.current = self.vision_list[self.index]

    def update_current(self) -> int:
        """
        Switches the current vision according to the value read from the update location given
        :return: the index received
        """
        new_idx = self.connection.receive_from_location(network_location=self.update_location or {})
        if type(new_idx) is int:
            self.switch_vision(new_idx)
            return new_idx
        return self.index

    def start(self, yield_ratios=False) -> Generator[Tuple[List[np.ndarray], np.ndarray, Any], None, None]:
        """
        A function that starts an infinite generator that takes an image
        detects with the current vision and returns the list of contours the image and directions
        and should be used as follows:
             for directions, contours, image in multi_vision.start():
                 # do something with the generated data
                 # like sending the data or displaying the contours
                 multi_vision.send(directions)
                 ovl.display_contours(image)
        :param yield_ratios: if True also yields the list of ratios returned from
        :yields: contours image directions and ratios if yield_ratios if True
        """
        while True:
            self.update_current()
            filtered_image = self.current.get_filtered_image()
            detection_result = self.current.detect(filtered_image, return_ratios=yield_ratios)
            contours = detection_result[0]
            image = detection_result[1]
            directions = self.current.director.direct(contours, image, self.current.camera_settings)
            if self.is_ambient():
                self.current.update_vision()
            yield (directions, *detection_result)
