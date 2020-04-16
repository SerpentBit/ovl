# Copyright 2018 - 2019 Ori Ben-Moshe - All rights reserved.
from typing import Any, Union
from threading import Thread
import uuid
import platform
import numpy as np
import cv2


class Camera:
    __slots__ = ("stream", "name", "grabbed", "frame", "stopped", "camera_thread", "start_immediately")

    def __init__(self, source: Union[str, int, cv2.VideoCapture] = 0,
                 image_width: int = 320, image_height: int = 240, start_immediately=True):
        """
        :param source: the source of the camera, can be a number, a device name or any valid source
                       for the cv2.VideoCapture object.
        :param image_width: the width of images to be captured in pixels
        :param image_height: the height of images to be captured in pixels
        """
        self.stream = cv2.VideoCapture(source)
        self.name = uuid.uuid4()

        if image_width:
            self.stream.set(3, image_width)
        if image_height:
            self.stream.set(4, image_height)
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False
        self.camera_thread: Union[None, Thread] = None
        self.start_immediately = start_immediately
        if start_immediately:
            self.start()

    def set_exposure(self, exposure_value) -> None:
        """
         Sets the exposure for the camera.
        Value range depend on the camera some use the value as the exponential so negative values
        :param exposure_value:
        """
        return self.stream.set(15, exposure_value)

    def start(self) -> "Camera":
        """
        starts the image taking thread
        :return: itself
        """
        if self.stopped:
            return self
        self.stopped = False
        self.camera_thread = Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """
        Takes a new image while not stopped
        :return:
        """
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()

    def read(self) -> [bool, np.ndarray]:
        """
         Returns the ret val and the frame
        :return: if the image was taken successfully, the image numpy
        :rtype: bool, numpy.array
        """
        return self.grabbed, self.frame

    def stop(self) -> None:
        """
        Stops the camera thread.
        """
        self.stopped = True

    def release(self) -> None:
        """
         stops the camera thread and releases the camera
        :return: None
        """
        self.stopped = True
        self.stream.release()

    def set(self, property_id: int, value) -> None:
        """
         sets the value of the given property to the given value
         :param property_id: the property number, for more information:
                        https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html
        :param value: the value to be set, a number
        :return: None
        """
        self.stream.set(property_id, value)

    def get(self, property_id) -> Any:
        """
         retrieves the value of a property based on its id
        :param property_id: the property number, for more information:
                        https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html
        :return: the value
        """
        if isinstance(property_id, int):
            raise ValueError("Given Property id {} was not valid, please refer to the documentation: "
                             "https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html".format(property_id))
        if not 0 <= type(property_id) < 19:
            raise ValueError("Invalid property id ({}), please refer to the documentation".format(property_id))
        return self.stream.get(property_id)

    def isOpened(self) -> bool:
        """
        Returns true_shape if the camera is opened and false_shapes otherwise
        :return: if the camera is open
        """
        return self.stream.isOpened()

    def getBackendName(self) -> str:
        """
        :return: returns the backend name of a camera
        :raises: SystemError on windows
        """
        if platform.system() == "Windows":
            raise SystemError("This method only available on Linux Operating Systems.")
        return self.stream.getBackendName()
