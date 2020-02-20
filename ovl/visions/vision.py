# Copyright 2018 - 2019 Ori Ben-Moshe - All rights reserved.
from functools import reduce
import time
import math
import copy
import types
import cv2
import numpy as np
import json
from typing import List, Union, Tuple, Any

from ..thresholds.color_ import built_in_colors
from ..exceptions_.exceptions import InvalidCustomFunctionError, CameraError
from ..camera_.camera import Camera
from ..partials.filter_applier import filter_applier
from ..thresholds.threshold import Threshold
from ..thresholds.color_.color import Color
from ..connections.connection import Connection
from ..directions_.director import Director
from ..camera_.camera_settings import CameraSettings
from ..connections.network_location import NetworkLocation
from ..directions_.directing_functions import center_directions


class Vision:
    """
    The Vision object represents the specifications to detect an object in an image.
    It performs the detection using a Threshold and filter functions.

    Additional capabilities and tuning options are:
        Image filters (Blurs, rotations, cropping),
        Morphological functions,
        Ovl color HSVCalibration,


    """
    def __init__(self, threshold: Threshold = None, contour_filters: List[types.FunctionType] = None,
                 director: Director = None, width=320, height=240, connection: Connection = None,
                 camera: Union[int, str, Camera, cv2.VideoCapture, Any] = None,
                 camera_settings: CameraSettings = None, morphological_functions: List[types.FunctionType] = None,
                 image_filters: List[types.FunctionType] = None, ovl_camera: bool = False, calibration: str = None):
        """
        The object that represents the pipeline of processing, detection, direction of values
        A connection object can be passed
        :param threshold: threshold object, creates the binary mask from a given image
        :param contour_filters: the list of contour_filter functions that
                                remove contours that aren't the target(s)
        :param director: a functions that receives a list or a single contour and returns director
        :param width: the width (in pixels) of images taken with the camera
        :param height: the height (in pixels)
        :param connection: a connection object that passes the result to the connection target
        :param camera: a Camera object (cv2.VideoCapture, ovl.Camera) or source from which to open a camera
        :param camera_settings: Special camera settings like calibration or offset used for
                                image correction and various direction calculations.
        :param morphological_functions: morphological functions used to apply on the binary
                               mask generated by the Threshold.
        :param image_filters: a list of image altering functions that are applied on the image.
        :param ovl_camera: a boolean that makes the camera opened to be ovl.Camera instead of cv2.VideoCapture
        :param calibration: a dictionary containing color calibration (HSVCalibration) coefficients and intercepts,
                            used for applying the calibration on the vision object
        """
        self.width = width
        self.height = height
        self.threshold = threshold
        self.contour_filters = contour_filters or []
        self.director = director or Director(center_directions, failed_detection=9999, target_amount=1)
        self.connection = connection
        self.image_filters = image_filters or []
        self.morphological_functions = morphological_functions or []
        self.camera = None
        self.camera_port = None
        self.camera_settings = camera_settings
        if isinstance(camera, (cv2.VideoCapture, Camera)):
            self.camera = camera
        elif camera is None:
            pass
        else:
            self.camera_setup(camera, width, height, ovl_camera=ovl_camera)

        self.calibration_path = None
        if calibration:
            self.calibration_path = calibration
            calibration = json.load(calibration)
            self.saturation_weight = calibration['saturation'] if 'saturation' in calibration else None
            self.brightness_weight = calibration['brightness'] if 'brightness' in calibration else None

    def __repr__(self):
        return str(self)

    def __str__(self):
        filters = [filter_function.__name__ for filter_function in self.contour_filters]
        threshold = self.threshold
        return "Vision: \n Threshold: {} \n Filters: {}".format(threshold, filters)

    @property
    def target_amount(self):
        """
        The wanted amount of targets
        (0 None or math.inf if there is no limit, 1 if 1 target is wanted etc.)
        """
        if self.director is None:
            return math.inf
        return self.director.target_amount

    def apply_morphological_functions(self, mask, morphological_functions=None):
        """
        Applies all morphological functions on the mask
        :param mask: the mask on which the functions should be applied
        :param morphological_functions: list of morphological_functions to be
                             applied instead of self.morphological_functions
        :return: the applied mask
        """
        if type(self.morphological_functions) not in (tuple, list, set):
            return mask
        morphological_functions = morphological_functions or self.morphological_functions
        return reduce(filter_applier, morphological_functions, mask)

    def send(self, data, *args, **kwargs) -> Union[None, Any]:
        """
        Sends data to the destination.
        :param data: The data to send to the Connection
        :param args: any other arguments for the send function in your connection
        :param kwargs: any other named arguments for the connection object
        :return: True if data was successfully sent, False if not.
        """
        return self.connection.send(*args, **kwargs, data=data)

    def send_to_location(self, data, network_location: NetworkLocation, *args, **kwargs):
        return self.connection.send_to_location(data, network_location, *args, **kwargs)

    def get_image(self) -> np.ndarray:
        """
        Gets an image from self.camera and applies image filters
        :return: the image, false if failed to get it
        """
        if self.camera is None:
            raise CameraError("No camera given, (Camera is None)")
        if not self.camera.isOpened():
            raise CameraError("Camera given is not open (Has it been closed or disconnected?)")
        output = self.camera.read()
        if len(output) == 2:
            ret, image = output
            return image if ret else False
        else:
            return output

    def get_filtered_image(self):
        """
        Gets an image from self.camera and applies all image filters
        :return: the image filter applied image
        """
        output = self.get_image()
        return self.apply_image_filters(output)

    def apply_filter(self, filter_function, contours, verbose=False):
        """
        Applies a filter function of the contour list
        :param filter_function: Filter functions are function with a contour list variable that apply some
        sort of filter on the contours, thus removing ones that don't fit the limit given by the filter.
        for example: straight_rectangle_filter removes contours that are not rectangles that are parallel to the frame
        of the picture
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

    def apply_all_filters(self, contours: List[np.ndarray], verbose=False
                          ) -> Tuple[List[np.ndarray], List[float]]:
        """
         Applies all of the filters on a list of contours
        :param contours: List of contours (numpy arrays) to
        :param verbose: prints out information about filtering process if true (useful for debugging)
        :return: a list of all of the ratios given by the filter function in order.
        """
        ratios = []
        for filter_func in self.contour_filters:
            contours, ratio = self.apply_filter(filter_func, contours, verbose=verbose)
            ratios.append(ratio)
        if verbose:
            print("After all filters: {}".format(len(contours)))
        return contours, ratios

    def apply_image_filters(self, image: np.ndarray) -> np.ndarray:
        """
         applies all given image filters to the given image
        :param image: the image that the image filters should be applied on (numpy array)
        :return: the image with the filters applied
        """
        return reduce(filter_applier, self.image_filters, image)

    def apply_threshold(self, image: np.ndarray, threshold=None) -> np.ndarray:
        """
         gets a mask for a given img and Threshold object (uses self.Threshold if given threshold was none)
        :param image: the numpy array of the image
        :param threshold: the Threshold object used to create the binary mask
        :return: the binary mask
        """
        threshold = threshold or self.threshold
        return threshold.convert(image)

    def find_contours_in_mask(self, mask: np.ndarray, return_hierarchy=False, apply_morphs=True
                              ) -> List[np.ndarray]:
        """
         gets contours from the given mask and apply
        :param mask: binary image (mask), a numpy array
        :param return_hierarchy: if the hierarchy should be returned
        :param apply_morphs: if the morphological functions should be applied.
        :return: the list of contours
        """
        mask = self.apply_morphological_functions(mask) if apply_morphs else mask
        result = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(result) == 3:
            _, contours, hierarchy = result
        elif len(result) == 2:
            contours, hierarchy = result
        else:
            raise ValueError("Invalid output from cv2.findContours, check that your cv2 (OpenCV) version is supported")
        return (contours, hierarchy) if return_hierarchy else contours

    def find_contours(self, image: np.ndarray, threshold=None, return_hierarchy=False) -> List[np.ndarray]:
        """
         Gets a list of all the contours within the threshold that was given
        :param threshold: the threshold that determines the binary masks
        :param image: image from which to get the contours
        :param return_hierarchy: if the hierarchy should be returned
        :return: list of all contours matching the range of hsv colours
        :rtype: list
        """
        threshold = threshold or self.threshold
        image_mask = self.apply_threshold(image, threshold=threshold)
        return self.find_contours_in_mask(image_mask, return_hierarchy=return_hierarchy)

    def get_directions(self, contours: List[np.ndarray], image: np.ndarray, sorter=None):
        """
        Calculates the directions, based on contours found in the given image
        :param contours: final contours after filtering
        :param image: the image from which to find the contours
        :param sorter: optional parameter, applies a sorter on the given contours
        :return: a string of the director (output of the director function),
                 length depends on the director function
        """
        return self.director.direct(contours, image, camera_settings=self.camera_settings, sorter=sorter)

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
            robot_cam = Camera(source=source, image_width=image_width, image_height=image_height)
        else:
            robot_cam = cv2.VideoCapture(source)
            if image_width != -1:
                robot_cam.set(3, image_width)
            if image_height != -1:
                robot_cam.set(4, image_height)

        if not robot_cam.isOpened():
            raise CameraError("Camera did not open correctly! Camera source: {}".format(self.camera_port))
        self.camera = robot_cam
        return robot_cam

    def apply_on_sample(self, image: Union[np.ndarray, str], threshold: Threshold = None, display_result: bool = False,
                        delay=0, result_color: Color = built_in_colors.RED_HIGH_HSV, return_hierarchy=False
                        ) -> Tuple[List[np.ndarray], np.ndarray]:
        """
         Finds contours and applies filters on a single image given by a image path or image object (numpy array)
        :param image: an image on which to apply the vision object
        :param threshold: a custom threshold can be passed
        :param display_result: if the contours found should be displayed
        :param delay: waitKey delay (0 if not in a loop, non-zero if it is)
        :param result_color: the colour of the contour outline
        :param return_hierarchy: if the contour hierarchies should be return
        :return: the image (numpy array) and the contours found (list of numpy arrays)
                 Can also return the hierarchies if return_hierarchy is true
        """
        threshold = threshold or self.threshold
        image = cv2.imread(image) if type(image) == str else image
        contours, hierarchy = self.find_contours(image, threshold, return_hierarchy)
        if display_result:
            image_for_display = copy.copy(image)
            cv2.drawContours(image_for_display, contours, -1, result_color)
            cv2.imshow(str(time.time()), image_for_display)
            cv2.waitKey(delay)
        return (contours, image, hierarchy) if return_hierarchy else (contours, image)

    def detect(self, image, verbose=False, return_ratios=False):
        """
        Gets contours and applies all filters and returns the result, thus detecting the object according
        to the specifications in the vision
        :param image: image in which the vision should detect an object
        :param verbose: If information about the filtering should be printed
        :param return_ratios: if the ratios from the filters should be returned
        :return: contours and the filtered image and the ratios if return_ratios is true
        """
        image = self.apply_image_filters(image)
        contours = self.find_contours(image)
        contours, ratios = self.apply_all_filters(contours, verbose)
        return (contours, image, ratios) if return_ratios else (contours, image)
