# Copyright 2018 Ori Ben-Moshe - All rights reserved.
import json
from numpy import ndarray, array
import copy
import cv2
import General
from sys import version_info

if version_info[0] is 3:
    xrange = range


class Color(object):

    @staticmethod
    def json_serialize(color_object):
        translate = {'high': color_object.high_bound,
                     'low': color_object.low_bound,
                     'color_space': color_object.color_space}
        return translate

    def pack(self):
        return json.dumps(Color.json_serialize(self))

    @property
    def low_h(self):
        return self.low[0]

    @property
    def low_s(self):
        return self.low[1]

    @property
    def low_v(self):
        return self.low[2]

    @property
    def high_h(self):
        return self.high[0]

    @property
    def high_s(self):
        return self.high[1]

    @property
    def high_v(self):
        return self.high[2]

    @staticmethod
    def unpack(json_string):
        d = json.loads(json_string)
        try:
            if type(d['sensitivity']) not in [int, float]:
                return False
            if not Color.assert_hsv(d['high']):
                return False
            if not Color.assert_hsv(d['low']):
                return False
        except TypeError:
            return False
        except ValueError:
            return False
        except KeyError:
            return False
        return Color(low=d['low'], high=d['high'])

    @staticmethod
    def deserialize(color_dict):
        d = color_dict
        try:
            if type(d['sensitivity']) not in [int, float]:
                return False
            if not Color.assert_hsv(d['high']):
                return False
            if not Color.assert_hsv(d['low']):
                return False

        except TypeError:
            return False
        except ValueError:
            return False
        except KeyError:
            return False
        return Color(low=d['low'], high=d['high'])

    def __repr__(self):
        return 'Color(' + str(self.low).replace("'", '') + ', ' + str(self.high).replace("'", '') + ')'

    def copy(self):
        return copy.copy(self)

    @property
    def low_bound(self):
        if type(self.__low_bound) is ndarray:
            return self.low_bound.to_list()
        return self.__low_bound

    @property
    def high_bound(self):
        if type(self.__low_bound) is ndarray:
            return self.low_bound.to_list()
        return self.__high_bound

    @staticmethod
    def validate(val, ceiling):
        """
        Action: Checks if val is positive and less than the ceiling value.
        :param val: The value to be checked (usually an int)
        :param ceiling: The highest value "val" can be. (usually an int)
        :return: True if val is less than ceiling and not negative
        """
        if ceiling <= 0:
            raise ValueError("Ceiling needs to be a positive value larger than 0.")
        val = int(val)
        return 0 <= val < ceiling

    @staticmethod
    def assert_hsv(hsv_point):
        """
        Action: Makes sure the hsv point(or vector) given in the parameter has valid values.
        :param hsv_point: a 3 length list with 3 ints describing a point the hsv color space
        that describe a color limit in a range for a findContour function.
        :return: True if valid False if not.
        :rtype: bool
        """
        return Color.validate(hsv_point[0], 180) and Color.validate(hsv_point[1], 256) and Color.validate(hsv_point[2],
                                                                                                          256)

    @staticmethod
    def apply_vector(point, vector, add=True):
        """
        Action: adds or subtracts a vector (value change) to a point (a hsv color limit).
        :param point: The hsv limit as a list of [h value, s value, v value].
        :param vector: The change to be made as a list of [h change, s change, v change].
        :param add: a boolean that when false subtracts the point and the vector instead of adding them.
        :return: the sum (or difference) of the point and the vector.
        :rtype: list
        """
        if add:
            result = list(map(int.__add__, point, vector))
            if Color.assert_hsv(result):
                return result
            raise ValueError("HSV limit out of range!")
        else:
            result = list(map(int.__sub__, point, vector))
            if Color.assert_hsv(result):
                return result
            raise ValueError("HSV limit out of range!")

    def apply_vector_low(self, vector, add=True):
        """
        Action: adds or subtracts a vector (value change) to the low limit of the Color (a hsv color limit).
        NOTE: AUTOMATICALLY UPDATES THE ATTRIBUTE IN THE COLOR OBJECT
        :param vector: The change to be made as a list of [h change, s change, v change].
        :param add: a boolean that when false subtracts the point and the vector instead of adding them.
        :return: the sum (or difference) of the point and the vector.
        :rtype: list
        """
        if add:
            result = list(map(int.__add__, self.__low_bound, vector))
            if Color.assert_hsv(result):
                return Color(result, self.__high_bound)
            raise ValueError("HSV limit out of range!")
        else:
            result = list(map(int.__sub__, self.__low_bound, vector))
            if Color.assert_hsv(result):
                return Color(result, self.__high_bound)
            raise ValueError("HSV limit out of range!")

    def apply_vector_high(self, vector, add=True):
        """
        Action: adds or subtracts a vector (value change) to the low limit of the Color (a hsv color limit).
        NOTE: AUTOMATICALLY UPDATES THE ATTRIBUTE IN THE COLOR OBJECT
        :param vector: The change to be made as a list of [h change, s change, v change].
        :param add: a boolean that when false subtracts the point and the vector instead of adding them.
        :return: the sum (or difference) of the point and the vector.
        :rtype: list
        """
        if add:
            result = list(map(int.__add__, self.__high_bound, vector))
            if Color.assert_hsv(result):
                return Color(self.__low_bound, result)
            raise ValueError("HSV limit out of range!")
        else:
            result = list(map(int.__sub__, self.__high_bound, vector))
            if Color.assert_hsv(result):
                return Color(self.__low_bound, result)
            raise ValueError("HSV limit out of range!")

    def set_low(self, new_range):
        point = self.copy()
        point = point.apply_vector_low(self.low_bound, False)
        return point.apply_vector_low(new_range)

    def set_high(self, new_range):
        point = self.copy()
        point = point.apply_vector_high(self.high_bound, False)
        return point.apply_vector_high(new_range)

    class ConstantError(TypeError):
        pass

    const_list = ["yellow_hsv",
                  'blue_hsv',
                  "orange_hsv",
                  'purple_hsv',
                  "white_hsv",
                  "black_hsv",
                  "blue_hsv",
                  "green_hsv",
                  "grey_hsv",
                  "red_low_hsv",
                  "teal_hsv",
                  "red_high_hsv"]

    def __init__(self, low, high):
        """
        Action: Constructor for the Color class
        :param high: high hsv limit of the color
        :param low: low hsv limit of the color
        """
        if type(low) is tuple:
            low = list(low)
        if type(high) is tuple:
            high = list(high)
        self.__low_bound = array(low)
        self.__high_bound = array(high)
        self.color_space = 'hsv'

    @property
    def low(self):
        """
        Action: Returns the low hsv limit of the color.
        :return: An uint8 numpy array with the low limit of the color.
        :rtype: uint8 numpy array
        """
        return self.__low_bound

    @property
    def high(self):
        """
        Action: Returns the high hsv limit of the color.
        :return: An uint8 numpy array with the high limit of the color.
        :rtype: uint8 numpy array
        """
        return self.__high_bound

    def light(self, amount=50):
        """
        Action: returns a copy of the color with a change in S low limit according to the given amount, default is 50
        NOTE: FOR HSV COLOR SPACE ONLY
        :return: the changed Color object
        """
        point = self.copy()
        point = point.apply_vector_low([0, -amount, 0])
        Color.assert_hsv(point.low)
        return point

    def dark(self, amount=50):
        """
        Action: returns a copy of the color with a change in S low limit according to the given amount, default is 50
        NOTE: FOR HSV COLOR SPACE ONLY
        :return: the changed Color object
        """
        point = self.copy()
        point.apply_vector_low([0, 0, -amount])
        Color.assert_hsv(point.low)
        return point

    def __str__(self):
        return str(self.low) + ' ' + str(self.high)


class MultiColor(object):

    def __init__(self, colors):
        """
        Action
        :param colors:
        """
        self.colors = colors
        for idx, r in enumerate(colors):
            if type(r) in (list, tuple):
                self.colors[idx] = Color(r[0], r[1])
            elif type(r) is Color:
                pass

    def pack(self):
        return json.dumps(MultiColor.json_serialize(self))

    @staticmethod
    def json_serialize(multi_color_object):
        return [Color.json_serialize(c) for c in multi_color_object.colors]

    def __str__(self):
        return ', '.join([str(color) for color in self.colors])

    def __repr__(self):
        return General.numerical_replace('MultiColor(0)', [repr(i) for i in self.colors]).replace("'", '')

    def adapt(self, img):
        for color in self.colors:
            color.adapt(img)

    @staticmethod
    def get_contours_for_range(img, color, vision):
        """
        Action: Gets a list of all the contours within the range that.
        :param color: a Color object describing (or numpy uint8 array) of color limit range in the hsv format.
        :param img: image from which to get the contours.
        :param vision: the vision object with a calibration to read from
        :return: list of all contours matching the range of hsv colours.
        :rtype: list, single numpy array (single contour) or None if no contour was found.
        """
        # If there was a problem reading the image, exit
        if img is None:
            raise Exception("No picture given!")
        hsv_low, hsv_high = color.low, color.high

        if vision.saturation_weight_vector is not None:
            image_mean = cv2.mean(img)[1]
            new_s = General.get_calibrated_value(image_mean, vision.saturation_weight_vector)
            hsv_low[1] = new_s

        if vision.value_weight_vector is not None:
            image_mean = cv2.mean(img)[2]
            new_v = General.get_calibrated_value(image_mean, vision.value_weight_vector)
            hsv_low[2] = new_v

        img_in_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_mask = cv2.inRange(img_in_hsv, hsv_low, hsv_high)

        if cv2.__version__.startswith("3."):
            return cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        if cv2.__version__.startswith("4."):
            return cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        elif cv2.__version__.startswith("2."):
            return cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        else:
            raise General.VersionError("This code works with version 2 and 3 of openCV!")

    def get_contours(self, img, vision):
        """
        Gets contours for all the color ranges in the multi color range object from the given picture.
        :param img: image from which to detect the contours according to the color ranges
        :param vision: the vision object
        :return: a list of the contours found for all of the
        """
        contours = []
        for color in self.colors:
            result = MultiColor.get_contours_for_range(img, color=color, vision=vision)
            if type(result) is list:
                contours.extend(result)
            elif type(result) is ndarray:
                contours.append(result)
            else:
                pass
        return contours

    def light(self, amount=50):
        """
        Action: Uses the .light() function on all of the colors in the MultiColors.
        :param amount: The amount to be subtracted from each color's low saturation value
        :return: None
        """
        for idx, color_range in enumerate(self.colors):
            self.colors[idx] = color_range.light(amount)

    def dark(self, amount=50):
        """
        Action: Uses the .light() function on all of the colors in the MultiColors.
        :param amount: The amount to be subtracted from each color's low value value
        :return: None
        """
        for idx, color_range in enumerate(self.colors):
            self.colors[idx] = color_range.dark(amount)


class BuiltInColors(General.ToolClass):
    """
    A list of Built in colors for the use of colour based contour vision,
    can use as a base colour for a custom colour (using the apply hsv vector method of the
    color class or as a color on its own.
    All colours as static variables of the BuiltInColors class and can be accessed:
    BuiltInColors.<color name>_hsv
    The BuiltInColor class is a resource class with a bunch of built-in ready to use
    colors. These Colors can be used as a base for custom made colours using the Color
    class' method apply_hsv_vector (or one of the low or high specific functions)
    using a vector as a parameter to the method [h, s, v].
    List of colors:
      Red (MultiColorObject) : Red (low) + Red (high)
      Red (Low): [0, 100, 100], [8, 255, 255]
      Red (High): [172, 100, 100], [179, 255, 255]
      Note: in order to find red, use both ranges (low and high) and use the some of both results.
      Blue: [105, 100, 100], [135, 255, 255]
      Green: [45, 100, 100], [75, 255, 255]
      Yellow: [15, 100, 100], [45, 255, 255]
      Orange: [10, 100, 100], [20, 255, 255]
      Grey: [0, 0, 0], [179, 50, 195]
      Black: [0, 0, 0], [179, 255, 30]
      White: [0, 0, 200], [179, 20, 255]
      Teal: [110, 100, 100], [130, 255, 255]
      Purple: [135, 100, 100], [165, 255, 255]
    """
    yellow_hsv = Color([25, 100, 100], [55, 255, 255])
    blue_hsv = Color([100, 100, 100], [135, 255, 255])
    green_hsv = Color([35, 100, 100], [75, 255, 255])
    purple_hsv = Color([130, 100, 100], [170, 255, 255])
    orange_hsv = Color([10, 100, 100], [25, 255, 255])
    red_low_hsv = Color([0, 100, 100], [15, 255, 255])
    red_high_hsv = Color([170, 100, 100], [179, 255, 255])
    red_hsv = MultiColor([red_high_hsv, red_low_hsv])
    white_hsv = Color([0, 0, 200], [179, 20, 255])
    black_hsv = Color([110, 0, 0], [130, 255, 30])
    grey_hsv = Color([0, 0, 0], [179, 50, 195])
    teal_hsv = Color([80, 50, 60], [95, 255, 155])

    built_in_list = [yellow_hsv,
                     blue_hsv,
                     green_hsv,
                     grey_hsv,
                     purple_hsv,
                     orange_hsv,
                     red_hsv,
                     white_hsv,
                     black_hsv,
                     teal_hsv]

