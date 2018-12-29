# Copyright 2018 Ori Ben-Moshe - All rights reserved.
from socket import *
from numpy import copy, vstack, hstack, ndarray
from Color import Color, BuiltInColors, MultiColor
from General import *
import Sorters
import time
from matplotlib.pyplot import figure, show, imshow
import copy
from inspect import getmembers, isfunction
import cv2
import json
from networktables import NetworkTables
from sys import version_info

if version_info[0] == 3:
    xrange = range


def display_image(image, win_name='image', resizable=False):
    """
    Action: The function displays the image whose path is received.
    :param image: Represents an image path (string), an already open image in the for of a numpy array (ndarray)
                  or a list of images
    :param win_name: Name of the Window that displays the images
    :param resizable: A boolean that determines whether the image window is resizable or not
    :return: None
    """
    if type(image) is str:
        img = cv2.imread(image)
        if resizable:
            cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
        cv2.imshow(win_name, img)
        cv2.waitKey()
    elif type(image) is ndarray:
        if resizable:
            cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
        cv2.imshow(win_name, image)
        cv2.waitKey()
    if type(image) is list:
        if type(image[0]) is str:
            image[0] = cv2.imread(image[0])
        shape = image[0].shape
        width = shape[0]
        height = shape[1]
        blob = image[0]
        for img in image[1:]:
            if type(img) is str:
                img = cv2.imread(img)
            im_shape = img.shape
            if width + im_shape[0] > height + im_shape[1]:
                blob = vstack((blob, img))
                width = im_shape[0]
            else:
                blob = hstack((blob, img))
                height += im_shape[1]
        if resizable:
            cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
        cv2.imshow(win_name, blob)
        cv2.waitKey()


class InvalidImage(object):

    def __init__(self):
        self.false = False

    def __bool__(self):
        return self.false


def get_all_functions():
    """
    Action: Returns a list of all available functions within the current scope
    :return: list of function object that are callable
    """
    f_list = []
    for module, module_object in globals().items():
        for sub_object_name, sub_object in getmembers(module_object):
            if isfunction(sub_object):
                f_list.append((sub_object_name, sub_object))
                continue
            for sub_members_name, sub_members_objects in getmembers(sub_object):
                if isfunction(sub_members_objects):
                    f_list.append((sub_members_name, sub_members_objects))
    return f_list


class Vision(object):
    """
    The vision object represents a control object to the whole process of the vision processing
    it receives  a list of filter functions, a directions function, the connection destination address,
    a port (or key) to connect to, list of parameters for the filter functions and 2 LinearDiscriminantAnalysis vectors.
    """

    NT_CONNECTION = 'NT'  # Network Tables via pynetworktables
    BT_CONNECTION = 'BT'  # BlueTooth via Socket, Not Impelented
    UDP_CONNECTION = 'UDP'  # UDP via Socket  
    TCP_CONNECTION = 'TCP'  # TCP via Socket, Not Impelented
    SERIAL_PORT = 'SP'  # Serial Port via 

    list_of_functions = get_all_functions()

    @staticmethod
    def is_static_ip(ip):
        """
        Action: checks if the given ip is a static ip for FRC
        :param ip: the ip to be checked, a str
        :return: True if the ip is an FRC static ip, False if it isn't
        """
        if type(ip) != str:
            return False
        if len(ip) == 10:
            if ip.startswith('10.') and ip.endswith('.2') and ip.count('.') == 3:
                return True
        return False

    @property
    def contour_amount(self):
        return len(self.contours)

    class FilterReplacement:
        def __init__(self, name):
            self.name = name

        def __name__(self):
            return self.name

    def get_filters(self):
        """
        Action: returns the list of filter functions
        :return:
        """
        return self.__filters

    def get_params(self):
        """
        Action: returns the list of the parameters for the filter functions
        :return:
        """
        return self.__params

    @staticmethod
    def is_valid_ip(ip):
        """
        Action: checks if the given ip address (string) is a valid ip
        :param ip: the string of the ip to be checked, can be ipv6 and ipv4
        :return: False if invalid, True if valid
        """
        try:
            inet_aton(ip)
            return True
        except error:
            return False

    def __del__(self):
        if self.camera is not None:
           self.camera.close()

    def __init__(self,color=None, filters=None, directions_function=None, target_amount=1, width=320, height=240,
                 connection_dst='NOCONNECTION', port=None, log_file=None, **kwargs):
        """
        Action: The vision object represents a control object to the whole process of the vision processing
        it receives  a list of filter functions, a directions function, the connection destination address,
        a UDP port to connect to, list of parameters for the filter functions and 2 vectors.
        :param filters: the list of filter functions
        :param directions_function: a functions that receives a list or a single contour and returns directions
        :param connection_dst: the connection (ip or hostname) in the network to connect to.
        :param port: the port number for the connection.
        :param log_file: a path to a file where output should be displayed
        :param kwargs: The optional key word arguments are: 
                       parameters for specific parameters for filter functions,
        """
        if log_file is not None:
            self.log_path = log_file
            if type(self.log_path) not in (str, bool, type(None)):
                raise TypeError('Invalid log file type, must be a file path, bool or None')
            if self.log_path is False:
                self.log_path = None
        else:
            self.log_path = None

        self.width = width
        self.height = height
        if type(width) != int:
            raise TypeError('The width of images taken must be an integer')
        if type(height) != int:
            raise TypeError('The width of images taken must be an integer')
            
        if filters is None:
            self.__filters = []
        else:
            self.__filters = filters
            if len(filters) == 0:
                print_pipe(self.log_path, "No filters given, Using raw contour result.")
        if "parameters" in kwargs:
            self.__params = kwargs['parameters']
        elif "params" in kwargs:
            self.__params = kwargs['params']
        else:
            self.__params = None

        target_amount = int(target_amount)
        if type(target_amount) is not int:
            self.target_amount = 1
        elif target_amount <= 0:
            self.target_amount = 0
        else:
            self.target_amount = target_amount

        self.contours = []
        self.socket = socket(AF_INET, SOCK_DGRAM)

        self.camera = None
        self.camera_port = None
        if 'camera_port' in kwargs:
            if type(kwargs['camera_port']) is int:
                self.camera_setup(kwargs['camera_port'])
        self.directions = directions_function

         if type(color_parameter) is Color:
             self.color = color_parameter
             self.low = color_parameter.low
             self.high = color_parameter.high
        elif type(color_parameter) is MultiColor:
            self.color = color_parameter
        else:
            raise print_pipe("The color parameter must be a Color or MultiRange object,"
                             "in order to use a color list use the hsv_high_limit and hsv_low_limit")
        # Calibration configuration
        if 'calibration' in kwargs:
            cal_file = kwargs['calibration']
            if type(cal_file) is str:
                if not cal_file.endswith('.json'):
                    raise ValueError('Calibration file is not a json file')
                with open(cal_file, 'r') as calibration_file:
                    cal = json.loads(calibration_file.read())
                    self.saturation_weight_vector = cal['swv']
                    self.value_weight_vector = cal['vwv']
        else:
            self.value_weight_vector = None
            self.saturation_weight_vector = None
            if 'svw' in kwargs:
                self.saturation_weight_vector = kwargs['swv']

            if 'vwv' in kwargs:
                    self.value_weight_vector = kwargs['vwv']
                    
        # Value returned if failed to find the target.
        if 'failed_value' in kwargs:
            self.failed_value = kwargs['failed_value']
            if type(self.failed_value) is int:
                self.failed_value = str(self.failed_value)
        else:
            self.failed_value = '9999'

        # Network related configurations
        self.hostname = connection_dst
        if connection_dst == 'NOCONNECTION':
            self.connection_address = None
            self.network_port = 0
        elif Vision.is_static_ip(connection_dst):
                self.connection_address= connection_dst
                NetworkTables.initialize(server=connection_dst)
                self.socket = NetworkTables.getTable('SmartDashboard')
                self.connection_type = 'NT'
                self.network_port = port
        elif connection_dst is None:
            self.connection_address = None
        elif Vision.is_valid_ip(connection_dst):
            if 0 < port < 65535:
                self.network_port = port
            else:
                self.network_port = 0
                raise TypeError("Invalid port number!")
            try:
                self.connection_address = connection_dst
                self.socket.bind((connection_dst, port))
            except Exception as e:
                print_pipe(self.log_path, 'Failed to connect.', e)
        else:
            if 0 < port < 65535:
                self.network_port = port
            else:
                self.network_port = 0
                raise TypeError("Invalid port number!")
            try:
                self.connection_address = gethostbyname(connection_dst)
            except gaierror:
                self.connection_address = False
                raise ValueError('Cannot Find Roborio, check the connection or the RoboRio name!')

    def apply_sorter(self, sorter_function=Sorters.descending_area_sort):
        """
        Action: applies a sorter function to the contour list
        :param sorter_function: the sorter function to be applied
        :return: the contour list (list of numpy arrays)
        """
        self.contours = sorter_function(self.contours)
        return self.contours

    def send_to_destination(self, data):
        """
        Action: Sends data to the destination.
        :param data: The data to send to the Roborio - Usually rhe directions calculated by the direction function
        :return: True if data was successfully sent, False if not.
        """
        if self.connection_type == Vision.NT_CONNECTION:
            self.socket.putNumber(self.network_port, data)
        elif self.connection_type == Vision.UDP_CONNECTION:
            self.socket.sendto(str(data), (self.connection_address, self.network_port))
        else:
            pass

    def apply_filter(self, filter_function, apply_results=False, parameters=None):
        """
        Action: applies a filter function of the contour list
        :param filter_function: Filter functions are function with a contour list variable that apply some
        sort of filter on the contours, thus removing ones that don't fit the limit given by the filter.
        for example: straight_rectangle_filter removes contours that are not rectangles that are parallel to the edges
        of the picture.
        :param apply_results: If you want to apply a filter only to debug and only see its affects without it affecting
        the contour
        :param parameters: Additional parameters for the function, uses the repr of the each parameter, the additional
         is in addition to the.
        :return: returns the output of the filter function.
        """

        print_pipe(self.log_path,
                   'Before "%": '.replace('%', filter_function.__name__.replace('_', ' ')) + str(len(self.contours)))
        if self.__params is not None or parameters is not None:
            if parameters is not None:
                parameters_list = parameters
            else:
                parameters_list = self.__params
            parameters_list.insert(0, self.contours)
            o = filter_function(*parameters_list)
        else:
            o = filter_function(self.contours)
        if type(o) is tuple:
            if len(o) == 2:
                output, ratio = o[0], o[1]
            else:
                raise InvalidCustomError('Filter function must return between 1 and 2 lists.'
                                         'Please refer to the Documentation: https://github.com/1937Elysium/Ovl-Python')
        elif type(o) in (list, ndarray):
            output, ratio = o, []
        else:
            raise TypeError('The contour list must be a list or a ndarray')

        if apply_results:
            if type(output) not in (list, ndarray):
                raise TypeError("Filter function must return a contour or a contour list!")
            self.contours = output
        print_pipe(self.log_path, 'After %: '.replace('%', filter_function.__name__) + str(len(output)))
        return output, ratio

    def apply_all_filters(self, apply_all=True):
        """
        Action: Applies all of the filters on the
        :param apply_all: A Boolean that determines whether or not apply all filters.
        :return: a list of all of the ratios given by the filter function in order.
        """
        all_ratios = []
        for idx, filter_func in enumerate(self.__filters):
            if self.__params is not None:
                _, ratio = self.apply_filter(filter_func, apply_results=apply_all, parameters=self.__params[idx])
                all_ratios.append(ratio)
            else:
                _, ratio = self.apply_filter(filter_func, apply_results=apply_all)
                all_ratios.append(ratio)

        return all_ratios

    def get_contours(self, img, color=None, save=True):
        """
        Action: Gets a list of all the contours within the range that
        NOTE: This method is only used for Color objects, for MultiColorRange please refer to the MultiColorRange
        class.
        :param color: a color object of the range to be detected
        :param img: image from which to get the contours
        :param save: if the contours returned from this function should be saved as self.contours
        :return: list of all contours matching the range of hsv colours
        :rtype: list
        """

        if color is not None:
            c = color
        else:
            c = self.color
        # If there was a problem reading the image, exit
        if img is None:
            raise Exception("No picture given!")

        if type(img) is str:
            img = cv2.imread(img)

        if self.saturation_weight_vector is not None:
            image_mean = cv2.mean(img)[1]
            new_s = get_calibrated_value(image_mean, self.saturation_weight_vector)
            c.low[1] = new_s

        if self.value_weight_vector is not None:
            image_mean = cv2.mean(img)[2]
            new_v = get_calibrated_value(image_mean, self.value_weight_vector)
            c.low[2] = new_v

        img_in_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        if type(c) == MultiColor:
            img_mask = cv2.inRange(img_in_hsv, c.colors[0].low, c.colors[0].high)
            for color_range in c.colors[1:]:
                img_mask += cv2.inRange(img_in_hsv, color_range.low, color_range.high)
        else:
            img_mask = cv2.inRange(img_in_hsv, c.low, c.high)

        if cv2.__version__.startswith("3."):
            found_contours = cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
            if save:
                self.contours = found_contours
            return found_contours
        elif cv2.__version__.startswith("4."):
            found_contours = cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
            if save:
                self.contours = found_contours
            return found_contours
        elif cv2.__version__.startswith("2."):
            found_contours = cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
            if save:
                self.contours = found_contours
            return found_contours
        else:
            raise VersionError("This code works only with version 2, 3 and 4 of openCV!")

    def __filter_list(self):
        """
        Action: returns a __repr__ of the filter function list
        :return: string of the list of filter functions
        """
        return str([f.__name__ for f in self.__filters]).replace("'", '')

    @staticmethod
    def get_match(func):
        """
        returns the matching function of the given function name (string)
        :param func: string of the name of a function
        :return: a function object by the name given
        """
        for m, n in Vision.list_of_functions:
            if isfunction(n):
                if str(func) == str(m):
                    return n

    def __repr__(self):
        """
        Action: Returns a string with the python code representing the Vision Object
        :return:
        """
        color = self.color.__repr__()
        filters = self.__filter_list()
        params = self.__params
        directions = self.directions.__name__

        return numerical_replace('Vision(color=0, '
                                 'filters=1, '
                                 'directions_function=3, '
                                 'parameters=2, '
                                 'target_amount=4, '
                                 'width=5, '
                                 'height=6, '
                                 'roborio_name=7, '
                                 'port=8,'
                                 'camera_port=9, '
                                 'failed_value=#, '
                                 'swv=$,'
                                 'vwv=^)',
                                 color,
                                 filters,
                                 params,
                                 directions,
                                 self.target_amount,
                                 self.width,
                                 self.height,
                                 self.hostname,
                                 self.network_port,
                                 self.camera_port).replace('#', str(self.failed_value))\
                                                  .replace('$', self.saturation_weight_vector.__repr__)\
                                                  .replace('^', self.value_weight_vector.__repr__)

    def __str__(self):
        """
        Action: Recaps the data in the Vision object, useful for debugging
        :return: string of the recap
        """
        filters_for_print = []
        for filter_obj in self.__filters:
            if type(filter_obj) == str:
                filters_for_print.append(filter_obj)
            if filter_obj is None:
                pass
            else:
                filters_for_print.append(filter_obj.__name__)
        filters = zip(filters_for_print, self.__params)
        ct = type(self.color)
        if ct is MultiColor:
            color_type = 'Multiple Color Range (MultiColor)'
        elif ct is Color:
            color_type = 'Single Color Range Object (Color)'
        else:
            color_type = 'Unknown'

        string = 'Vision Recap:\n' \
                 'Filters & custom Parameters: 0\n' \
                 'Color Detection Type: 1\n' \
                 'Color: 2\n' \
                 'Directions Function:9 \n' \
                 'Target Amount:8 \n' \
                 'Connection:\n' \
                 'Connection Address or IP: 3\n' \
                 'Connection Port: 4\n\n' \
                 'Camera:\n' \
                 'Camera port: 5\n' \
                 'Image Width & Height: 6, 7\n' \
                 'Failed Value:\n' \
                 'Log File:\n'
        return numerical_replace(string,
                                 filters,
                                 color_type,
                                 self.color.__repr__(),
                                 self.connection_address,
                                 self.network_port,
                                 self.camera_port,
                                 self.width,
                                 self.height,
                                 self.directions_function.__name__,
                                 self.target_amount)

    def get_directions(self, contours, amount=None, directions_function=None, sorter=Sorters.descending_area_sort):
        """
        Action: Calculates the directions based on contours found
        :param contours: final contours after filtering
        :param amount: amount of final contours, this should be the amount of objects  you want to detect
        :param directions_function: optional parameter, a different directions function from the one defined
                                    in the Vision object.
        :param sorter: optional parameter,
        :return: a string of the directions (output of the directions function),
                 length depends on the directions function
        """
        if amount is None:
            amount = self.target_amount
        if sorter is not None:
            target_contours = sorter(contours)[0:amount]
        else:
            target_contours = contours[0:amount]
        if directions_function is None:
            return self.directions(target_contours, amount, (self.width, self.height))
        else:
            return directions_function(target_contours, amount, (self.width, self.height))

    def camera_setup(self, port=0, img_width=None, img_height=None):
        """
        Action: Opens up the camera reference and fixates a given width and height to all images taken
        :param img_width: the width of the images to be taken
        :param img_height: the height of the images to be taken
        :param port: the camera port
        :return: the camera object, also sets self.camera to the object.
        """
        if img_height is None:
            img_height = self.height
        if img_width is None:
            img_width = self.width
        if type(port) is not int:
            port = 0
        self.camera_port = port
        robot_cam = cv2.VideoCapture(port)
        # If there was a problem opening the camera, exit
        if robot_cam.isOpened() is False:
            raise Exception("An error has occurred! "
                            "cv2.VideoCapture returned None (Camera object unsuccessfully opened!")
        # Checks in which cv version we use and adjusts accordingly
        if cv2.__version__.startswith("3."):
            robot_cam.set(cv2.CAP_PROP_FRAME_WIDTH, img_width)
            robot_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, img_height)
        elif cv2.__version__.startswith("4."):
            robot_cam.set(cv2.CAP_PROP_FRAME_WIDTH, img_width)
            robot_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, img_height)
        elif cv2.__version__.startswith("2."):
            robot_cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, img_width)
            robot_cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, img_height)
        else:
            raise VersionError("This code works with version 2 and 3 of openCV!"
                               " Please make sure you are using one of those versions")
        self.camera = robot_cam
        return robot_cam

    def apply_sample(self, **kwargs):
        """
        Action: Finds contours and applies filters on a single image given by a image path, image object (numpy array)
        or camera port and takes an image, a custom color can be passed through the kw color.
        the kw display/show determines how the result is displayed, None will not display, False with imshow, True with
        matlplotlib.
        :param kwargs:
        :return: the image (numpy array) and the contours found (list of numpy arrays)
        """
        def cam_port_activate(port_val, color, wid, hgt):
            if self.camera is None:
                self.camera_setup(port_val, img_width=wid, img_height=hgt)
            return_val, image = self.camera.read()
            if return_val:
                self.contours = self.get_contours(image, color)
                self.apply_all_filters()
            else:
                print_pipe(self.log_path, "Something went wrong with getting the sample image!")
            return self.contours, image

        def image_activate(image_loc, color):
            if type(image_loc) is str:
                image = cv2.imread(image_loc, cv2.IMREAD_COLOR)
            else:
                image = image_loc
                self.contours = self.get_contours(image, color)
                self.apply_all_filters()
            return self.contours, image

        multi_mode = False
        if "color" in kwargs:
            color_object = kwargs["color"]
            if type(color_object) is MultiColor:
                multi_mode = True
        elif "hsv_low_limit" in kwargs and "hsv_high_limit" in kwargs:
            color_object = Color(kwargs["hsv_low_limit"], kwargs["hsv_high_limit"])
        else:
            if type(self.color) is MultiColor:
                multi_mode = True
            color_object = self.color

        if "display" in kwargs:
            display = kwargs["display"]
        elif "show" in kwargs:
            display = kwargs["show"]
        else:
            display = None

        if "camera_port" in kwargs:
            port = kwargs["camera_port"]
            contours, img = cam_port_activate(port, color_object, self.width, self.height)
        elif "port" in kwargs:
            port = kwargs["port"]
            contours, img = cam_port_activate(port, color_object, self.width, self.height)
        elif "image" in kwargs:
            contours, img = image_activate(kwargs["image"], color_object)
        elif "img" in kwargs:
            contours, img = image_activate(kwargs["img"], color_object)
        elif "pic" in kwargs:
            contours, img = image_activate(kwargs["pic"], color_object)
        elif "picture" in kwargs:
            contours, img = image_activate(kwargs["picture"], color_object)
        else:
            raise ValueError("No image or camera port given!")

        if display is not None:
            image_for_display = copy.copy(img)
            drawn = cv2.drawContours(image_for_display, contours, -1, BuiltInColors.red_high_hsv.high_bound)
            if display:
                figure(str(time.time()))
                image_for_display = cv2.cvtColor(drawn, cv2.COLOR_HSV2RGB)
                imshow(image_for_display)
                show()
            else:
                cv2.imshow(str(time.time()), image_for_display)
                cv2.waitKey()
        return contours, img

    class DoubleStack:
        def __init__(self):
            self.class1 = 0
            self.class2 = 0

        def inc1(self):
            self.class1 += 1

        def inc2(self):
            self.class2 += 1

        def bigger(self):
            if self.class1 > self.class2:
                return 1
            if self.class1 == self.class2:
                return 3
            return 2

        def sum(self):
            return self.class2 + self.class1

    def single_frame(self, port=0, apply_all=True):
        """
        Action: gets contours and applies all filters and returns the result
        :param port: port of the camera
        :param apply_all: if filters should be applied and have an effect on the contour list
        :return: contours, ratio list (from the filter functions)
        """
        if self.camera is None:
            self.camera_setup(port, self.width, self.height)
        return_val, new_img = self.camera.read()
        if return_val:
            self.contours = self.get_contours(new_img)
            r = self.apply_all_filters(apply_all)
            return self.contours, r
        else:
            print_pipe(self.log_path, 'Failed to get image')

    def frame_loop(self, apply_all=True, one_loop=False, print_results=True,
                   send_direction=True, amend=True):
        """
        Action: frame loop: Takes an image, finds contours, applies all filters and sorters, finds direction and sends
                the direction to the RoboRIO in an infinite loop, amends for bad frames.
        :param apply_all: if filters should be applied
        :param one_loop: if loop should be executed once.
        :param print_results: if results should be printed through the pipe.
        :param send_direction: If directions should be sent to the RoboRIO.
        :param amend: If Bad frames should be amended by using previous values.
        :return: None
        """
        previous_result = None
        streak = Vision.DoubleStack()
        while True:
            old_time = time.time()
            for frame_num in xrange(30):
                return_val, new_img = self.camera.read()
                if return_val:
                    self.contours = self.get_contours(new_img)
                    self.apply_all_filters(apply_all=apply_all)
                    directions = self.directions(self.contours, self.target_amount, new_img)
                    if directions is False:
                        if previous_result is not None and amend:
                            directions = previous_result
                            streak.inc2()
                        elif previous_result is None:
                            self.send_to_destination(self.failed_value)
                            if print_results:
                                print_pipe(self.log_path, self.failed_value)
                            continue
                    if print_results:
                        print_pipe(self.log_path, directions)
                    if send_direction:
                        self.send_to_destination(directions)
                else:
                    if not one_loop:
                        print_pipe(self.log_path, "%d was an invalid picture!" % frame_num)
                    else:
                        print_pipe(self.log_path, "invalid picture!")
                    if previous_result is not None and amend:
                        streak.inc2()
                        directions = previous_result
                        if print_results:
                            print_pipe(self.log_path, directions)
                        if send_direction and self.roborio_ip is not None:
                            self.send_to_destination(directions)
                if streak.sum() > 3 and print_results:
                    res = streak.bigger()
                    if res is 1:
                        print_pipe(self.log_path,
                                   'Warning: The last {0} iterations have failed.'
                                   ' In {1} of them not enough contours were found to perform the directions function.'
                                   ''.format(streak.sum(), streak.class1))
                    if res is 2:
                        print_pipe(self.log_path,
                                   'Warning: The last {0} iterations have failed.'
                                   ' In {1} of them the camera failed to take an image.'
                                   ''.format(streak.sum(), streak.class2))
                    if res is 3:
                        print_pipe(self.log_path,
                                   'Warning: The last {0} iterations have failed.'
                                   ' In {1} of them the camera failed to take an image'
                                   ' and in {1} of them not enough contours were found.'
                                   ''.format(streak.sum(), streak.class2))
            if print_results:
                print_pipe(self.log_path, "Completed 30 frames in ", time.time() - old_time)
            if one_loop:
                break

    def start(self, **kwargs):
        """
        Action: Sets up the camera and activates the loop, find contours in an image, filter, get direction
        :param kwargs:
        :return: None
        """
        if "camera" in kwargs:
            port, width, height = kwargs["camera"]
        elif "cam" in kwargs:
            port, width, height = kwargs["cam"]
        else:
            port, width, height = 0, self.width, self.height
        if type(self.camera) is not cv2.VideoCapture:
            self.camera_setup(port, img_width=width, img_height=height)
        while True:
            self.frame_loop()

    def __call__(self, **kwargs):
        self.start(**kwargs)

    def translate_parameters(self):
        """
        Translates parameters to a json save-able format, capable of translating Color and MultiColor objects too.
        :return: the dictionary with the translated parameters for filter functions
        """
        param_copy = copy.copy(self.__params)
        for idx1, param_list in enumerate(param_copy):
            for idx2, val in enumerate(param_list):
                if type(val) is Color:
                    param_copy[idx1][idx2] = Color.json_serialize(val)
                if type(val) is MultiColor:
                    param_copy[idx1][idx2] = MultiColor.json_serialize(val)
        return param_copy

    def json_serialize(self, pass_camera=False, pass_network=False, pass_calibration=False):
        """
        Action: Translates the Vision object to a Json file for transportability
        :param pass_camera: a bool denoting if the camera parameters (camera port) should be serialized.
        :param pass_network: a bool denoting if the network parameters and connection information (port, connection type and
                             destination should be serialized as well.
        :param pass_calibration: a bool denoting if the calibration parameters (vectors and means) should be serialized.
        :return: the serialized string in json format.
        """
        if type(pass_network) is not bool:
            pass_network = False
        if type(pass_camera) is not bool:
            pass_camera = False
        if type(pass_calibration) is not bool:
            pass_calibration = False
        if type(self.color) is Color:
            color_object = Color.json_serialize(self.color)
        elif type(self.color) is MultiColor:
            color_object = MultiColor.json_serialize(self.color)
        else:
            raise TypeError('Color is not a color or MultiColor!')
        translation = {'color': color_object,
                       'filters': [f.__name__ for f in self.__filters],
                       'parameters': self.translate_parameters(),
                       'directions_function': self.directions.__name__,
                       'target_amount': self.target_amount,
                       'width': self.width,
                       'height': self.height,
                       'calibration_information': pass_calibration,
                       'camera_information': pass_camera,
                       'network_information': pass_network}
        if pass_camera:
            translation['camera_port'] = self.camera_port
        if pass_network:
            translation['port'] = self.network_port
            translation['destination'] = self.roborio_name
            translation['connection_type'] = self.connection_type
        if pass_calibration:
            translation['v_vector'] = self.value_weight_vector
            translation['s_vector'] = self.saturation_weight_vector

        result = json.dumps(translation)
        return result

    @staticmethod
    def json_deserialize_secure(json_string):
        """
        NOTE: When opening json files acquired from the internet open in first with deserialize secure, if it doesn't
        return false, you can open it with json deserialize
        Action: Takes the content of a json file and turns opens it as a Vision Object
        :param json_string: A string of json data.
        :return: The dictionary containing the deserialized data (python objects)
        """
        deserialized = json.loads(json_string)
        d = deserialized
        if type(deserialized) is not dict:
            return False

        try:
            color = Color.deserialize(d['color'])
            if color is False:
                return False
            filters = [Vision.get_match(f) for f in d['filters'] if type(f) == str]
            params = d['parameters']
            for idx1, parameter_list in enumerate(params):
                for idx2, val in enumerate(parameter_list):
                    if type(val) is list:
                        params[idx1][idx2] = [Color.deserialize(c_object) for c_object in val if type(c_object) is dict]
                    elif type(val) is dict:
                        params[idx1][idx2] = Color.deserialize(val)
            directions = d['directions_function']
            if type(directions) is False:
                return False
            target_amount = d['target_amount']
            width = d['width']
            height = d['height']
            if type(width) is not int:
                return False
            if type(height) is not int:
                return False
            cam_port = None
            if d['camera_information'] is True:
                cam_port = d['camera_port']
                if not (type(cam_port) is int or cam_port is None):
                    return False
            roborio_name = 'NOCONNECTION'
            port = 9212
            nw = d['network_information']
            if nw is True:
                port = d['port']
                roborio_name = d['roborio_name']
                if type(port) is not int:
                    return False
                if type(roborio_name) != str:
                    return False
        except Exception as e:
            if e:
                pass
            return False
        if nw:
            return Vision(color=color,
                          filters=filters,
                          directions_function=directions,
                          port=port,
                          parameters=params,
                          camera_port=cam_port,
                          width=width,
                          height=height,
                          connection_dst=roborio_name,
                          target_amount=target_amount)
        return Vision(color=color,
                      filters=filters,
                      parameters=params,
                      target_amount=target_amount,
                      directions_function=directions,
                      camera_port=cam_port,
                      width=width,
                      height=height)

    @staticmethod
    def json_deserialize(json_string):
        """
        Action: Takes the content of a json file and turns opens it as a Vision Object
        :param json_string: A string of json data.
        :return: The dictionary containing the deserialized data (python objects)
        """
        deserialized = json.loads(json_string)
        d = deserialized
        color = Color.deserialize(d['color'])
        filters = [f for f in d['filters'] if type(f) == str]
        params = d['parameters']
        for idx1, parameter_list in enumerate(params):
            for idx2, val in enumerate(parameter_list):
                if type(val) is list:
                    params[idx1][idx2] = [Color.deserialize(color_obj) for color_obj in val if type(color_obj) is dict]
                elif type(val) is dict:
                    params[idx1][idx2] = Color.deserialize(val)
        directions = d['directions_function']
        target_amount = d['target_amount']
        width = d['width']
        height = d['height']
        cam_port = None
        if d['camera_information'] is True:
            cam_port = d['camera_port']
        roborio_name = 'NOCONNECTION'
        port = 9212
        nw = d['network_information']
        if nw is True:
            port = d['port']
            roborio_name = d['roborio_name']
        nw = d['network_information']
        if nw:
            return Vision(color=color,
                          filters=filters,
                          directions_function=directions,
                          parameters=params,
                          port=port,
                          camera_port=cam_port,
                          width=width,
                          height=height,
                          connection_dst=roborio_name,
                          target_amount=target_amount)
        return Vision(color=color,
                      filters=filters,
                      parameters=params,
                      target_amount=target_amount,
                      directions_function=directions,
                      camera_port=cam_port,
                      width=width,
                      height=height)

    def pack(self, file_path, pass_network, pass_camera, pass_calibration):
        """
        Action: serializes and writes the vision object (self) to
        :param file_path: The path to file where the object should be saved, should be a json file.
        :param pass_camera: a bool denoting if the camera parameters (camera port) should be serialized.
        :param pass_network: a bool denoting if the network parameters and connection information (port, connection type
                             and destination should be serialized as well.
        :param pass_calibration: a bool denoting if the calibration parameters (vectors and means) should be serialized.
        :return: True if save and serialize was succesful false otherwise
        """
        if file_path.endswith('.json'):
            with open(file_path, 'w') as f:
                f.write(self.json_serialize(pass_network=pass_network,
                                            pass_calibration=pass_calibration,
                                            pass_camera=pass_camera))
                f.close()
            return True
        else:
            return False

    NC_NUMERAL = 'numeral'
    NC_TIME = 'time'

    def display_contours(self, img, amount=0, color=None, save_path=None):
        """
        Action: Displays the image with the current list of contours
        :param img: image from which the contours were taken from, numpy array or image path
        :param color: the color of the of the contours outline
        :param amount: amount of contours to display
        :param save_path: if the image should be saved, pass the wanted result path
        :return: the image with the drawn contours.
        """
        if type(img) is str:
            img = cv2.imread(img)
        image_for_display = copy.copy(img)
        if self.contour_amount > 0:
            if amount > 0:
                output_contours = self.contours[0:amount]
            else:
                output_contours = self.contours

            if type(output_contours) is not list:
                output_contours = [output_contours]
            if color is None:
                color = (0, 0, 0)
            cv2.drawContours(image_for_display, output_contours, -1, color, 2)
        if type(save_path) is str:
            cv2.imwrite(save_path, image_for_display)
        display_image(image_for_display)
        return image_for_display

    def photo_array(self, amount, delay=3, name_convention=NC_TIME, return_images=False, path=False):
        """
        Action: Takes a series of images with a delay between shots and saves them.
        :param amount: the amount of images to take
        :param delay: the delay between images
        :param name_convention: the naming convention to save the pictures
        :param return_images: a boolean to denote if the image objects should be returned
        :param path: if images should be saved in a specific folder
        :return: if return images is true, returns the images
        """
        if self.camera is None:
            self.camera_setup()
        images = []
        image_num = 0
        while image_num < amount:
            ret, img = self.camera.read()
            if ret:
                images.append(img)
                if name_convention is Vision.NC_TIME:
                    save_name = 'image@ '.replace('@', str(image_num)) + \
                                str(time.strftime('%a%d%b%Y%H:%M:%S', time.gmtime()))
                elif name_convention is Vision.NC_NUMERAL:
                    save_name = 'image@'.replace('@', str(image_num))
                else:
                    save_name = str(name_convention) + str(image_num)
                if path:
                    save_name = str(path) + save_name
                cv2.imwrite(save_name, img)
                while True:
                    cv2.imshow('', img)
                    key = cv2.waitKey(delay)
                    if key == ord('y'):
                        amount += 1
                        break
                    elif key == ord('n'):
                        break
                    else:
                        pass

        if return_images:
            return images
        else:
            del images

    def rasses_vanegev(self, amount, delay=3, name_convention=NC_TIME, return_images=False, path=False):
        """
        Action: Takes a series of images with a delay between shots and saves them.
        :param self: a vision object
        :param amount: the amount of images to take
        :param delay: the delay between images
        :param name_convention: the naming convention to save the pictures
        :param return_images: a boolean to denote if the image objects should be returned
        :param path: if images should be saved in a specific folder
        :return: if return images is true, returns the images
        """
        return self.photo_array(amount, delay, name_convention, return_images, path)
