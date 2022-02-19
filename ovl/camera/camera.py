import time
from threading import Thread
from typing import Any, Union

import cv2
import numpy as np

from .camera_configuration import CameraConfiguration
from ..utils.constants import DEFAULT_IMAGE_HEIGHT, DEFAULT_IMAGE_WIDTH, DEFAULT_CAMERA_SOURCE, \
    MAX_OPENCV_CAMERA_PROPERTY, MIN_OPENCV_CAMERA_PROPERTY


def configure_camera(camera, configuration, delay=0):
    for camera_property, value in configuration.camera_properties.items():
        camera.set(camera_property, value)
        if delay:
            time.sleep(delay)


class Camera:
    __slots__ = ("stream", "grabbed", "frame", "stopped", "camera_thread", "start_immediately")

    def __init__(self, source: Union[str, int, cv2.VideoCapture] = DEFAULT_CAMERA_SOURCE,
                 image_width: int = DEFAULT_IMAGE_WIDTH, image_height: int = DEFAULT_IMAGE_HEIGHT,
                 start_immediately=True):
        """
        Camera connects to and opens a connected camera and on constantly reads image from the camera.
        ovl.Camera is more real-time oriented and operates at a faster rate than opencv's VideoCapture, but is not
        suited for non-infinite streams

        The connected camera can be opened by using a camera number (index), url of ip camera, device file (/dev/video0)

        Note: as a result of increasing fps, Camera is not fit for opening video files or any other
        definite frame form of video.

        :param source: The source of the camera, can be a number, a device name or any other valid source
        for the cv2.VideoCapture object.
        :param image_width: The width of images to be captured in pixels
        :param image_height: The height of images to be captured in pixels
        :param start_immediately: The Camera has an inner thread that reads images, this determines if
        it should start immediately or be started by `Camera.start` manually.
        """

        self.stream = cv2.VideoCapture(source)

        if image_width:
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, image_width)
        if image_height:
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, image_height)
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False
        self.camera_thread: Union[None, Thread] = None
        self.start_immediately = start_immediately
        if start_immediately:
            self.start()

    def set_exposure(self, exposure_value: float, *, configuration_delay: Union[int, float] = 0) -> bool:
        """
        Sets the exposure for the camera.
        Value range depend on the camera some use the value as the exponential negative values or actual number of ms

        :param exposure_value: the exposure value to be set
        :param configuration_delay: the time to wait after setting exposure for it to take effect
        :return: if it was successful in setting the value
        """
        setting_value = self.stream.set(cv2.CAP_PROP_EXPOSURE, exposure_value)
        if configuration_delay:
            time.sleep(configuration_delay)
        return setting_value

    def start(self) -> "Camera":
        """
        Starts the image taking thread

        :return: self
        """
        if self.stopped:
            return self
        self.stopped = False
        self.camera_thread = Thread(target=self._update).start()
        return self

    def _update(self) -> None:
        """
        Takes a new image while not stopped

        """
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()

    def read(self) -> [bool, np.ndarray]:
        """
        Returns the return value (if getting the frame was successful and the frame itself)

        This function is mainly for compatibility with cv2.VideoCapture, Camera.get_image() is
        recommended for common use.

        :return: if the image was taken successfully, the image
        :rtype: bool, `numpy.array`
        """
        return self.grabbed, self.frame

    def get_image(self) -> np.ndarray:
        """
        Returns the current image

        :return: numpy array of the image
        """
        return self.frame

    def stop(self) -> None:
        """
        Stops the camera thread.

        """
        self.stopped = True

    def release(self) -> None:
        """
        Stops the camera thread and releases the camera

        :return: None
        """
        self.stop()
        self.stream.release()

    def set(self, property_id: int, value: Union[float, bool, str, Any]) -> None:
        """
        Sets the value of the given property to the given value

        Properties are characteristics of the camera that can be changed to alter how images
        are returns, things from image width and height, contrast and saturation exposure etc.

        Not all cameras support all property changes, make sure the one you are using does.

        Read more at:
        https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html#aeb1644641842e6b104f244f049648f94

        import cv2 and use cv2.CAP_PROP_<PROPERTY NAME> or simply use the property id number. The number depends
        on the property's location f.e CAP_PROP_FRAME_WIDTH is 3

        :param property_id: the property id (number)
        :param value: the value to be set, a number
        :return: None
        """
        self.stream.set(property_id, value)

    def get(self, property_id) -> Any:
        """
        Retrieves the value of a property based on its id

        :param property_id: the property number, for more information:
                        https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html
        :return: the value of the property
        """
        if isinstance(property_id, int):
            raise ValueError(
                f"Given Property id {property_id} was not valid, please refer to the documentation: "
                f"https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html")
        if not MIN_OPENCV_CAMERA_PROPERTY <= type(property_id) <= MAX_OPENCV_CAMERA_PROPERTY:
            raise ValueError(f"Invalid property id ({property_id}), please refer to the documentation")
        return self.stream.get(property_id)

    def is_opened(self) -> bool:
        """
        Returns true_shape if the camera is opened, false otherwise

        :return: if the camera is open
        """
        return self.stream.isOpened()

    def isOpened(self) -> bool:
        """
        Returns true_shape if the camera is opened, false otherwise
        This function is left to allow it to be used wherever cv2.VideoCapture can be used

        :return: if the camera is open
        """
        return self.stream.isOpened()

    def get_backend_name(self) -> str:
        """
        Gets the backend name of the camera using cv2.VideoCapture.getBackendName()

        :return: returns the backend name of a camera
        """
        return self.stream.getBackendName()

    def getBackendName(self) -> str:
        """
        Gets the backend name of the camera using cv2.VideoCapture.getBackendName()

        This Function exists to allow compatibility with opencv's VideoCapture object
        :return: returns the backend name of a camera
        """
        return self.get_backend_name()

    def configure_camera(self, configuration: CameraConfiguration, delay=0):
        """
        Uses a camera configuration object to configure the camera, can use the configuration_delay parameter to wait after each set.

        :param configuration: a `CameraConfiguration` allows to configure a camera
        :param delay:  some properties can have a time configuration_delay in order to take effect,
         a configuration_delay in seconds can be added to wait after each configuration.
        """
        configure_camera(self.stream, configuration=configuration, delay=delay)
