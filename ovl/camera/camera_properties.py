from enum import Enum

import cv2


class CameraProperties(int, Enum):
    """
    An enum containing the various properties that can be configured for cameras,
    Different cameras support different apis, this means not all properties are supported for each camera, checking with
    the camera manufacturer and the drivers written in opencv determines what is supported,
    you're encouraged to test what options work for your camera beforehand.

    You can read more about each option at the opencv documentation here:

    Examples:


    Simply use the enum members as the keys to set various properties:

    e.g. setting camera exposure:

    .. code-block:: python

        import ovl

        camera = ovl.Camera(0)
        camera.set(CameraProperties.AUTO_EXPOSURE, 0)
        camera.set(CameraProperties.EXPOSURE, -12)


    Camera properties work both with ovl's `Camera` and with opencv's `VideoCapture`

    .. code-block:: python

        import cv2
        from ovl import CameraProperties

        camera = cv2.VideoCapture(0)

        camera.set(CameraProperties.IMAGE_WIDTH, 320)
        camera.set(CameraProperties.IMAGE_HEIGHT, 240)



    """
    IMAGE_WIDTH = cv2.CAP_PROP_FRAME_WIDTH
    IMAGE_HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
    CAMERA_FPS = cv2.CAP_PROP_FPS
    CAMERA_MODE = cv2.CAP_PROP_MODE
    BRIGHTNESS = cv2.CAP_PROP_BRIGHTNESS
    CONTRAST = cv2.CAP_PROP_CONTRAST
    SATURATION = cv2.CAP_PROP_SATURATION
    HUE = cv2.CAP_PROP_HUE
    GAIN = cv2.CAP_PROP_GAIN
    EXPOSURE = cv2.CAP_PROP_EXPOSURE
    MONOCHROME = cv2.CAP_PROP_MONOCHROME
    SHARPNESS = cv2.CAP_PROP_SHARPNESS
    AUTO_EXPOSURE = cv2.CAP_PROP_AUTO_EXPOSURE
