import math
import types
from functools import reduce
from logging import getLogger
from typing import List, Union, Any, Callable, Tuple, Iterable

import cv2
import numpy as np

from ovl import OMIT_DIMENSION_VALUES, DEFAULT_FAILED_DETECTION_VALUE, VISION_LOGGER
from utils.types import Target
from ..camera.camera import Camera, configure_camera
from ..camera.camera_configuration import CameraConfiguration
from ..detectors.detector import Detector
from ..directions.directing_functions import center_directions
from ..directions.director import Director
from ..exceptions.exceptions import CameraError, ImageError
from ..partials.filter_applier import apply
from ..thresholds.threshold import Threshold
from ..utils.constants import DEFAULT_IMAGE_HEIGHT, DEFAULT_IMAGE_WIDTH, BASE_LOGGER
from ..utils.get_function_name import get_function_name
from ..utils.vision_detector_arguments import arguments_to_detector

logger = getLogger(f"{BASE_LOGGER}.{VISION_LOGGER}")


class Vision:
    """
    Vision object represents a computer vision pipeline.
    The pipeline consists of 4 main stages:
         1. processing - 'apply_all_image_filters' which uses a list of image_filter functions
         2. detection - 'detect' which comes from Detector objects and detects objects (targets, bounding rectangles..)
         3. filtering  - 'apply_target_filters' which is uses filter_functions like contour_filters
         4. conversion & usage - 'direct' which comes from director objects

    Each functionality can be used to easily create a complex yet modular

    Additional capabilities and tuning options are:
        Image filters (Blurs, rotations, cropping),
        Morphological functions,

        1. camera handling
        2. connection clean-up and sending

    Vision can also be used as a part of a more complex pipeline.

    MultiVision can contain multiple vision objects and switch between pipelines, allowing for very versatile logic
    that can fit multiple needs.

    Ambient Vision is another option for using 2 different Vision objects and alternate between the 2.
    """

    def __init__(self, detector: Detector = None, threshold: Threshold = None,
                 morphological_functions: List[types.FunctionType] = None,
                 target_filters: List[types.FunctionType] = None, director: Director = None,
                 target_selector: Union[int, tuple, Callable] = 1,
                 width=DEFAULT_IMAGE_WIDTH, height=DEFAULT_IMAGE_HEIGHT,
                 camera: Union[int, str, Camera, cv2.VideoCapture, Any] = None,
                 camera_configuration: CameraConfiguration = None, image_filters: List[types.FunctionType] = None,
                 ovl_camera: bool = False, haar_classifier: str = None, logger_name: str = None):
        """
        :param detector: a Detector object responsible for detecting targets
        :param threshold: threshold is a shortcut for detecting
        :param target_filters: the list of target_filter functions that remove targets that aren't what you want,
        can also perform grouping, sorting or any other action you want to
        :param director: a functions that receive a list or a single contour and returns director
        :param width: the width (in pixels) of images taken with the camera
        :param height: the height (in pixels)
        :param camera: a Camera object (cv2.VideoCapture, ovl.Camera) or source from which to open a camera
        :param camera_configuration: Special camera settings like calibration or offset used for
                                image correction and various direction calculations.
        :param image_filters: a list of image altering functions that are applied on the image.
        :param ovl_camera: a boolean that makes the camera opened to be ovl.Camera instead of cv2.VideoCapture
        :param haar_classifier:
        :param target_selector: decides how many/what targets are selected after targets have been filtered
        """
        if not (detector is None and threshold is None and haar_classifier is None):
            mutually_exclusive_arguments = {"threshold": (threshold, morphological_functions),
                                            "detector": (detector,),
                                            "haar_cascade": (haar_classifier,)}

            detector = arguments_to_detector(mutually_exclusive_arguments)
        self.detector = detector

        self.width = width
        self.height = height
        self.target_filters = target_filters or []
        self.director = director or Director(center_directions,
                                             failed_detection=DEFAULT_FAILED_DETECTION_VALUE,
                                             target_selector=target_selector)
        self.image_filters = image_filters or []
        self.camera = None
        self.camera_port = None
        self.camera_configuration = camera_configuration
        self.logger = getLogger(logger_name or VISION_LOGGER)

        if isinstance(camera, (cv2.VideoCapture, Camera)) or camera is None:
            self.camera = camera
        else:
            self.camera_setup(camera, width, height, camera_configuration, ovl_camera=ovl_camera)

    def __repr__(self):
        return str(self)

    def __str__(self):
        filters = [get_function_name(filter_function) for filter_function in self.target_filters]
        image_filters = [get_function_name(image_filter) for image_filter in self.image_filters]
        return f"Vision: \n Detector: {self.detector} \n Filters: {filters} \n Image Filters: {image_filters}"

    @property
    def target_selector(self):
        """
        The wanted amount of targets
        Determined by `self.director`
        (0 None or math.inf if there is no limit, 1 if 1 target is wanted etc.)

        """
        if self.director is None:
            return math.inf
        return self.director.target_selector

    def get_image(self) -> np.ndarray:
        """
        Gets an image from `self.camera` and applies image filters

        :return: the image
        :raises: ImageError if the image fau

        """
        if self.camera is None:
            raise CameraError("No camera given, (Camera is None)")
        if not self.camera.isOpened():
            raise CameraError("The Vision's camera is not open (Has it been closed or disconnected?)")
        output = self.camera.read()
        if len(output) == 2:
            success, image = output
            if not success:
                raise ImageError("Failed to take image")
            return image
        else:
            return output

    def apply_target_filter(self, filter_function, targets):
        """
        Applies a filter function on the target list, this is used to remove targets
        that do not match desired features

        NOTE: `Vision.detect` is mainly used for full object detection and filtering,
        refer to it for common use of Vision

        :param filter_function: Filter functions are functions that take out targets that
         for example: straight_rectangle_filter removes contours that are not rectangles that are parallel
         to the frame of the picture
        :param targets: the targets on which the filter should be applied (list of numpy.ndarrays or bounding boxes,
        depends on the values returned by your detector)
        :return: returns the output of the filter function.

        """
        name = get_function_name(filter_function)
        self.logger.info(f'Before "{name}": {len(targets)}')
        filtered_targets = filter_function(targets)
        return filtered_targets

    def apply_target_filters(self, targets: Iterable["Target"]) -> Iterable["Target"]:
        """
        Applies all target filters on a list of targets, one after the other.
        Applies the first filter and passes the output to the second filter,

        :param targets: List of targets (numpy arrays or bounding boxes) to
        :return: a list of all ratios given by the filter functions in order.

        """
        return list(reduce(apply, self.target_filters, targets))

    def apply_image_filters(self, image: np.ndarray) -> np.ndarray:
        """
        Applies all given image filters to the given image
        This is used to apply various image filters on your image in a pipeline,
        like blurs, image cropping, contrasting, sharpening, rotations, translations etc.

        :param image: the image that the image filters should be applied on (numpy array)
        :return: the image with the filters applied
        """
        return reduce(apply, self.image_filters, image)

    def get_directions(self, targets: Iterable["Target"], image: np.ndarray) -> Any:
        """
        Calculates the directions, based on targets found in the given image

        :param targets: final targets after filtering
        :param image: the image
        :return: returns the direction
        """
        return self.director.direct(targets, image)

    def camera_setup(self, source=0, image_width=None, image_height=None,
                     camera_configuration: CameraConfiguration = None, ovl_camera=False):
        """
        Opens up the camera reference and sets a given width and height to all images taken

        :param image_width: the width of the images to be taken, 0 does not set a width
        :param image_height: the height of the images to be taken, 0 does not set a height
        :param camera_configuration: a camera configuration object that allows easy camera configuration of the various
        properties defined in `cv2.VideoCapture`. Depends on the camera you use and its driver.
        :param source: the location from which to open the camera
         string for network connections int for local USB connections.
        :param ovl_camera: if the camera object should be ovl.Camera
        :return: the camera object, also sets `self.camera`.
        """

        image_height = image_height or self.height
        image_width = image_width or self.width
        self.camera_port = source
        if ovl_camera:
            camera = Camera(source=source, image_width=image_width, image_height=image_height)
            self.width = image_width
            self.height = image_height

        else:
            camera = cv2.VideoCapture(source)
            if image_width not in OMIT_DIMENSION_VALUES:
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, image_width)
                self.width = image_width
            if image_height not in OMIT_DIMENSION_VALUES:
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, image_height)
                self.height = image_height

        if not camera.isOpened():
            raise CameraError(f"Camera did not open correctly! Camera source: {self.camera_port}")
        if camera_configuration is not None:
            configure_camera(camera, camera_configuration)
        self.camera = camera
        return camera

    def detect(self, image, *args, **kwargs) -> Tuple[Iterable["Target"], "np.ndarray"]:
        """
        This is the function that performs processing, detection and filtering on a given image, essentially passing
        the image through the detection related part of the pipeline

        `detect` applies image filters, detects objects in the filtered images
        (using the passed/created detector object)
        and finally applies all the target_filters on the image.

        args and kwargs are passed to the detect function (passed to the detect method of the detector)

        :param image: image in which the vision should detect an object
        :return: targets and the filtered image

        """
        filtered_image = self.apply_image_filters(image)
        targets = self.detector.detect(filtered_image, *args, **kwargs)
        filtered_targets = self.apply_target_filters(targets)
        return filtered_targets, filtered_image
