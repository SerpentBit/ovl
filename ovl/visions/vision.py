from functools import reduce
import math
import types
import cv2
import numpy as np
from typing import List, Union, Tuple, Any
from ..detectors.detector import Detector
from ..exceptions.exceptions import InvalidCustomFunctionError, CameraError
from ..camera.camera import Camera
from ..partials.filter_applier import filter_applier
from ..connections.connection import Connection
from ..directions.director import Director
from ..camera_.camera_settings import CameraSettings
from ..connections.network_location import NetworkLocation
from ..directions.directing_functions import center_directions


class Vision:
    """
    Vision object represents a computer vision pipeline.
    The pipeline consists of 4 main stages:
         1. processing - 'apply_all_image_filters' which uses a list of image_filter functions
         2. detection - 'detect' which comes from Detector objects and detects objects (contours, bounding rectangles..)
         3. filtering  - 'apply_target_filters' which is uses filter_functions like contour_filters
         4. conversion & usage - 'direct' which comes from director objects

    Each functionality can be used to easily create a complex yet modular

    Additional capabilities and tuning options are:
        Image filters (Blurs, rotations, cropping),
        Morphological functions,
        Ovl color HSVCalibration,

        1. camera handling
        2. connection clean-up and sending

    Vision can also be used as a part of a more complex pipeline.

    MultiVision can contain multiple vision objects and switch between pipelines, allowing for very versatile logic
    that can fit multiple needs.

    Ambient Vision is another option for using 2 different Vision objects and alternate between the 2.
    """

    def __init__(self, detector: Detector = None, target_filters: List[types.FunctionType] = None,
                 director: Director = None, width=320, height=240, connection: Connection = None,
                 camera: Union[int, str, Camera, cv2.VideoCapture, Any] = None,
                 camera_settings: CameraSettings = None, image_filters: List[types.FunctionType] = None,
                 ovl_camera: bool = False):
        """
        :param detector: a Detector object responsible
        :param target_filters: the list of contour_filter functions that
                                remove contours that aren't the target(s)
        :param director: a functions that receives a list or a single contour and returns director
        :param width: the width (in pixels) of images taken with the camera
        :param height: the height (in pixels)
        :param connection: a connection object that passes the result to the connection target
        :param camera: a Camera object (cv2.VideoCapture, ovl.Camera) or source from which to open a camera
        :param camera_settings: Special camera settings like calibration or offset used for
                                image correction and various direction calculations.
        :param image_filters: a list of image altering functions that are applied on the image.
        :param ovl_camera: a boolean that makes the camera opened to be ovl.Camera instead of cv2.VideoCapture
        """
        self.detector = detector
        self.width = width
        self.height = height
        self.target_filters = target_filters or []
        self.director = director or Director(center_directions, failed_detection=9999, target_amount=1)
        self.connection = connection
        self.image_filters = image_filters or []
        self.camera = None
        self.camera_port = None
        self.camera_settings = camera_settings
        if isinstance(camera, (cv2.VideoCapture, Camera)):
            self.camera = camera
        elif camera is None:
            pass
        else:
            self.camera_setup(camera, width, height, ovl_camera=ovl_camera)

    def __repr__(self):
        return str(self)

    def __str__(self):
        filters = [filter_function.__name__ for filter_function in self.target_filters]
        return "Vision: \n Detector: {} \n Filters: {}".format(self.detector, filters)

    @property
    def target_amount(self):
        """
        The wanted amount of targets
        Determined by self.director
        (0 None or math.inf if there is no limit, 1 if 1 target is wanted etc.)

        """
        if self.director is None:
            return math.inf
        return self.director.target_amount

    def send(self, data: Any, *args, **kwargs) -> Any:
        """
        Sends data to the destination using self.connection

        :param data: The data to send to the Connection
        :param args: any other arguments for the send function in your connection
        :param kwargs: any other named arguments for the connection object
        :return: Depends on the connection object used, returns its result

        """
        return self.connection.send(*args, **kwargs, data=data)

    def send_to_location(self, data: Any, network_location: NetworkLocation, *args, **kwargs):
        """
        A function that sends data to a specific NetworkLocation

        :param data: the data to be sent
        :param network_location: information used to send the data to a specific 'location'
         in the network
        :return: Depends on the connection object

        """
        return self.connection.send_to_location(data, network_location, *args, **kwargs)

    def get_image(self) -> np.ndarray:
        """
        Gets an image from self.camera and applies image filters

        :return: the image, false if failed to get it

        """
        if self.camera is None:
            raise ValueError("No camera given, (Camera is None)")
        if not self.camera.isOpened():
            raise CameraError("Camera given is not open (Has it been closed or disconnected?)")
        output = self.camera.read()
        if len(output) == 2:
            ret, image = output
            return image if ret else False
        else:
            return output

    def apply_target_filter(self, filter_function, contours, verbose=False):
        """
        Applies a filter function on the contour list, this is used to remove contours
        that do not match desired features

        NOTE: Vision.detect is mainly used for full object detection and filtering,
        refer to it for common use of Vision

        :param filter_function: Filter functions are function with a contour list variable that apply some
         sort of filter on the contours, thus removing ones that don't fit the limit given by the filter.
         for example: straight_rectangle_filter removes contours that are not rectangles that are parallel
         to the frame of the picture
        :param contours: the contours on which the filter should be applied (list of numpy.ndarrays)
        :param verbose: if true_shape does not print anything
        :return: returns the output of the filter function.

        """
        if verbose:
            print('Before "{}": {}'.format(filter_function.__name__, len(contours)))
        filter_function_output = filter_function(contours)

        if isinstance(filter_function_output, tuple):
            if len(filter_function_output) == 2:
                filtered_contours, ratio = filter_function_output[0], filter_function_output[1]
            else:
                raise InvalidCustomFunctionError('Filter function must return between 1 and 2 lists.'
                                                 'Please refer to the Documentation: '
                                                 'https://github.com/1937Elysium/Ovl-Python')
        elif isinstance(filter_function_output, list):
            filtered_contours, ratio = filter_function_output, []
        else:
            raise TypeError('The contour list must be a list or tuple of 2 lists (contours and ratios)')
        return filtered_contours, ratio

    def apply_target_filters(self, targets: List[np.ndarray], verbose=False
                             ) -> Tuple[List[np.ndarray], List[float]]:
        """
        Applies all of the filters on a list of contours, one after the other.
        Applies the first filter and passes the output to the second filter,

        :param targets: List of targets (numpy arrays or bounding boxes) to
        :param verbose: prints out information about filtering process if true (useful for debugging)
        :return: a list of all of the ratios given by the filter function in order.

        """
        ratios = []
        for filter_func in self.target_filters:
            targets, ratio = self.apply_target_filter(filter_func, targets, verbose=verbose)
            ratios.append(ratio)
        if verbose:
            print("After all filters: {}".format(len(targets)))
        return targets, ratios

    def apply_image_filters(self, image: np.ndarray) -> np.ndarray:
        """
        Applies all given image filters to the given image
        This is used to apply various image filters on your image in a pipeline,
        like blurs, image cropping, contrasting, sharpening, rotations, translations etc.

        :param image: the image that the image filters should be applied on (numpy array)
        :return: the image with the filters applied
        """
        return reduce(filter_applier, self.image_filters, image)

    def get_directions(self, contours: List[np.ndarray], image: np.ndarray, sorter=None):
        """
        Calculates the directions, based on contours found in the given image

        :param contours: final contours after filtering
        :param image: the image from which to find the contours
        :param sorter: optional parameter, applies a sorter on the given contours
        :return: a string of the director (output of the director function),
                 length depends on the director function
        """
        return self.director.direct(contours, image, sorter=sorter)

    def camera_setup(self, source=0, image_width=None, image_height=None, ovl_camera=False):
        """
        Opens up the camera reference and sets a given width and height to all images taken

        :param image_width: the width of the images to be taken, 0 does not set a width
        :param image_height: the height of the images to be taken, 0 does not set a height
        :param source: the location from which to open the camera
         string for network connections int for local USB connections.
        :param ovl_camera: if the camera object should be ovl.Camera
        :return: the camera object, also sets self.camera to the object.
        """

        image_height = image_height or self.height
        image_width = image_width or self.width
        self.camera_port = source
        if ovl_camera:
            camera = Camera(source=source, image_width=image_width, image_height=image_height)
        else:
            camera = cv2.VideoCapture(source)
            if image_width != -1:
                camera.set(3, image_width)
            if image_height != -1:
                camera.set(4, image_height)

        if not camera.isOpened():
            raise CameraError("Camera did not open correctly! Camera source: {}".format(self.camera_port))
        self.camera = camera
        return camera
