# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
import cv2
import json
from numpy import array

from ..thresholds.color_.color import Color
from ..thresholds.color_.multi_color import MultiColor

LinearDiscriminantAnalysis = None


class HSVCalibration(object):
    """
    The calibration object that executes the machine learning
    Order: (img_mean, lower_bound)
    """
    def __init__(self, vision, class_amount, filter_min_ratio=0.9, min_area=100):
        """
        HSVCalibration object is an object that preforms a HSVCalibration function and runs during setup.
        :param vision: The Vision process to be calibration, a Vision object or Vision Json
        :param class_amount: The amount of ranges to be taken from every range for every image per class
        :param filter_min_ratio: a list with the ratio for each filter or just a float, for custom value per filter
                                 function.
        :param min_area: the minimum area a contour must have
        :returns: The calibration object
        """
        self.vision = vision
        self.color = vision.color
        self.vision.filters.remove()

        if type(filter_min_ratio) is float:
            self.rating_ratio = filter_min_ratio ** len(self.vision.get_filters())
        elif type(filter_min_ratio) is list:
            for ratio in filter_min_ratio:
                self.rating_ratio *= ratio
        self.min_area = min_area
        self.class_amount = class_amount
        self.s_clf = None
        self.v_clf = None

    class ContourRating:
        def __init__(self, contour, rating):
            self.rating = rating
            self.area = cv2.contourArea(contour)

    def brute_force(self, img, color, start_v=25, start_s=13, s_buffer=20, v_buffer=20):
        """
        Action: Calculates the Rating of each contour that passes all of the filters
        :param img: The image from which the contours should be taken
        :param color: the color that
        :param start_v: the starting v value from which to iterate, should not be 0 or negative
        :param start_s: the starting s value from which to iterate, should not be 0 or negative
        :param s_buffer: a buffer on the lower bound of color from which to check all possibilities
        :param v_buffer: a buffer on the lower bound of color from which to check all possibilities
        :return:
        """
        s_values = color.low_s + v_buffer
        v_values = color.low_v + s_buffer
        if s_values > 255 or s_values < 0:
            raise ValueError('Invalid range value,"s" must be between 0 and 255 (s = lower s + given buffer)')
        if v_values > 255 or v_values < 0:
            raise ValueError('Invalid range value,"v" must be between 0 and 255 (v = lower v + given buffer)')
        h = color.low_h
        high_range = color.high_bound
        final_list = []
        for s in range(start_s, s_values + 1):
            for v in range(start_v, v_values + 1):
                current_range = Color([h, s, v], high_range)
                self.vision.contours = self.vision.get_contours(img, color=current_range)
                self.vision.apply_all_filters(apply_all=True)
                filter_ratio_product = self.vision.apply_all_filters(apply_all=False)
                ratings = [1] * len(self.vision.contours)
                for filter_ratio in filter_ratio_product:
                    for idx, r in enumerate(filter_ratio):
                        ratings[idx] *= HSVCalibration.ContourRating(self.vision.contours[idx], r)
                ratings.sort(key=lambda k: k.rating)
                if len(ratings) >= self.vision.target_amount:
                    fail = False
                    for contour_rating in ratings[0: self.vision.target_amount]:
                        if type(contour_rating) is HSVCalibration.ContourRating:
                            if contour_rating.area <= self.min_area:
                                fail = True
                            elif contour_rating.rating < self.rating_ratio:
                                fail = True
                    if fail:
                        final_list.append([current_range.low_bound, False])
                    else:
                        final_list.append([current_range.low_bound, ratings])
                else:
                    final_list.append([current_range.low_bound, False])

        return final_list

    def find_data(self, img_list, color=None, start_v=25, start_s=13, s_buffer=20, v_buffer=20):
        """
        Action: Finds Working and non working color ranges and turns them into a list
        :param img_list: list of images from which to calibrate
        :param color: the color object
        :param start_v: the minimum valid v value
        :param start_s: the minimum valid s value
        :param s_buffer: the additional value values to check below low value
        :param v_buffer: the additional saturation values to check below low value
        :return: the Classifiers for Saturation and Value and the numpy array of data
        """
        global LinearDiscriminantAnalysis
        if LinearDiscriminantAnalysis is None:
            from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

        if color is None:
            color = self.color

        def get_data_from_color(color_obj, img_obj, img_mean):
            s_data = []
            v_data = []
            s_classifier = []
            v_classifier = []
            rating_list = self.brute_force(img_obj, color_obj, start_v, start_s, s_buffer, v_buffer)
            class1 = 0
            class2 = 0

            for obj in rating_list[0:self.class_amount]:
                if type(obj) is list:
                    bound, rating = obj
                    s_data.append([img_mean[1], bound[1]])
                    s_classifier.append(1)
                    class1 += 1
                    v_data.append([img_mean[2], bound[2]])
                    v_classifier.append(1)
                    class1 += 1

            for bound, rating in rating_list:
                if rating is False and class2 < self.class_amount:
                    s_data.append([img_mean[1], bound[1]])
                    s_classifier.append(2)
                    class2 += 1
                    v_data.append([img_mean[2], bound[2]])
                    v_classifier.append(2)
                    class2 += 1
            return s_data, s_classifier, v_data, v_classifier

        if type(color) is Color:
            saturation_data, saturation_classes, value_data, value_classes = [], [], [], []
            for img in img_list:
                tmp = get_data_from_color(color, img, cv2.mean(img))
                tmp_saturation_data = tmp[0]
                tmp_saturation_classes = tmp[1]
                tmp_value_data = tmp[2]
                tmp_value_class = tmp[3]
                saturation_data.extend(tmp_saturation_data)
                saturation_classes.extend(tmp_saturation_classes)
                value_classes.extend(tmp_value_class)
                value_data.extend(tmp_value_data)
            if not (len(saturation_data) == len(saturation_classes) == len(value_classes) == len(value_data)):
                raise ValueError("Data isn't equal in size!")
            if saturation_data is []:
                raise ValueError("No data")
            self.s_clf = LinearDiscriminantAnalysis(solver='eigen')
            self.s_clf.fit(array(saturation_data), array(saturation_classes))
            self.v_clf = LinearDiscriminantAnalysis(solver='eigen')
            self.v_clf.fit(array(value_data), array(value_classes))

        elif type(color) is MultiColor:
            saturation_data, saturation_classes, value_data, value_classes = [], [], [], []
            for img in img_list:
                mean = cv2.mean(img)
                for color in color.colors:
                    tmp = get_data_from_color(color, img, mean)
                    tmp_saturation_data = tmp[0]
                    tmp_saturation_classes = tmp[1]
                    tmp_value_data = tmp[2]
                    tmp_value_class = tmp[3]
                    saturation_data.extend(tmp_saturation_data)
                    saturation_classes.extend(tmp_saturation_classes)
                    value_classes.extend(tmp_value_class)
                    value_data.extend(tmp_value_data)
            if not (len(saturation_data) == len(saturation_classes) == len(value_classes) == len(value_data)):
                raise ValueError("Data isn't equal in size!")
            if saturation_data is []:
                raise ValueError("No data")
            saturation_data, saturation_classes = array(saturation_data), array(saturation_classes)
            value_data, value_classes = array(value_data), array(value_classes)
            self.s_clf = LinearDiscriminantAnalysis(solver='eigen')
            self.s_clf.fit(saturation_data, saturation_classes)
            self.v_clf = LinearDiscriminantAnalysis(solver='eigen')
            self.v_clf.fit(value_data, value_classes)
            return self.s_clf, self.v_clf

    def json_serialize(self, file_name=None):
        """
        Action: Turns a Trained HSVCalibration object to a Json File for use in a Vision program
                And saves it as a json file
        :return: The Translation of the Object to Python
        """
        s_wc1, s_wc2 = self.s_clf.coef_[0]
        s_w_intercept = self.s_clf.intercept_
        s_mean = self.s_clf.means_

        v_wc1, v_wc2 = self.v_clf.coef_[0]
        v_w_intercept = self.v_clf.intercept_
        v_mean = self.v_clf.means_

        translation = {
            'saturation_weight_vector': {'coefficient1': s_wc1,
                                         'coefficient2': s_wc2,
                                         'inter': s_w_intercept,
                                         'mean': s_mean},
            'brightness_weight_vector': {'coefficient1': v_wc1,
                                         'coefficient2': v_wc2,
                                         'inter': v_w_intercept,
                                         'mean': v_mean}}
        if file_name is not None:
            if not file_name.endswith('.json'):
                print(None, 'Target file is not a json file')
            with open(file_name, 'r') as f:
                f.write(json.dumps(translation))
        return translation
