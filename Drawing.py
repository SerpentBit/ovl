# Copyright 2018 Ori Ben-Moshe - All rights reserved.
from math import cos, sin
from numpy import array, uint64, uint8, zeros
import cv2
import Geometry
from random import randint, choice, uniform
from Color import Color, MultiColor
import sys

if sys.version_info[0] == 3:
    xrange = range

GRADE_N = 0

GRADE_NW = 1

GRADE_W = 2

GRADE_SW = 3

GRADE_S = 4

GRADE_SE = 5

GRADE_E = 6

GRADE_NE = 7

GRADE_CENTER = 8

list_of_grades = [GRADE_N, GRADE_NW, GRADE_W, GRADE_SW, GRADE_S, GRADE_SE, GRADE_E, GRADE_NE]


class Shape(object):
    def __init__(self, drawing_function, amount, dimensions_ranges, color, gradient=(0.25, 4)):
        self.drawing_function = drawing_function
        self.amount = amount
        self.color = color
        self.tone = None
        self.dimensions = dimensions_ranges
        self.gradient = gradient

    def draw(self, image, img_width, img_height):
        for i in xrange(self.amount):
            if type(self.drawing_function) is list:
                df = choice(self.drawing_function)
            else:
                df = self.drawing_function
            point, dimensions = self.__random_dimensions(img_width, img_height)
            self.tone = self.__random_color()
            df(image, point, dimensions, self.tone, self.__random_gradient())

    def __random_color(self):
        def random_range(low, high):
            return [randint(low[0], high[0]), randint(low[1], high[1]), randint(low[2], high[2])]
        color_range = self.color
        cr_type = type(color_range)
        if cr_type is Color:
            return random_range(color_range.low, color_range.high)
        elif cr_type is MultiColor:
            h, s, v = [], [], []
            for color in color_range.colors:
                j = random_range(color.low, color.high)
                h.append(j[0])
                s.append(j[1])
                v.append(j[1])
            return [choice(h), choice(s), choice(v)]

    def __random_dimensions(self, width, height):
        if type(self.dimensions) not in (list, tuple):
            raise TypeError('Dimensions is not a list or tuple!')
        if type(self.dimensions[0]) not in (int, list, tuple):
            raise TypeError('Dimensions must be either a range by itself or a list of ranges!')
        list_type = type(self.dimensions[0])
        for obj in self.dimensions:
            if type(obj) is not list_type:
                raise TypeError('Dimensions must be a range or a list of ranges, not both')

        if list_type == int:
            size = randint(self.dimensions[0], self.dimensions[1])
            return (randint(size, width - size), randint(0 + size, height - size)), size
        if list_type == list:
            dimensions = []
            for dimension in self.dimensions:
                size = randint(dimension[0], dimension[1])
                dimensions.append(size)
            size = max(dimensions)
            point = (randint(size, width - size ), randint(size, height - size))
            return point, dimensions

    def __random_gradient(self, color_space='BGR'):
        if self.tone is None:
            return None
        if color_space in ['BGR', 'RGB']:
            gradient = []
            for i in self.tone:
                multi = 1
                if i > 127:
                    multi = -1
                gradient.append(multi)
            for idx, tone in enumerate(self.tone):
                if tone == 0:
                    self.tone[idx] = 1
            r1, r2 = self.tone[1] / self.tone[0], self.tone[2] / self.tone[0]
            r0 = round(uniform(gradient[0], gradient[1]), 3)
            r1 *= r0 * gradient[1]
            r2 *= r0 * gradient[2]
            r0 += gradient[0]
            b = str(randint(-5, 5))
            if color_space is 'RGB':
                return str(r2) + '* x + ' + b, str(r1) + '* x + ' + b, str(r0) + '* x + ' + b
            return str(r0) + '* x + ' + b, str(r1) + '* x + ' + b, str(r2) + '* x + ' + b


def gradient_circle(image, center, radius, color=(0, 0, 0), gradient=('2*x', '2*x', '2*x'), tangent_angle=0):
    """
    Action: Draws a circle with a gradient according to the given traits
    :param image: The that the circle should be drawn on, an already open image as a numpy array (opened with cv2.imread)
    :param center: the center of the circle a tuple in the form of (x,y), in pixels, (0,0) is the top left corner
    :param radius: the radius of the circle to be drawn, in pixels
    :param color: the starting color of the circle, in the color space of the image
    :param gradient: the change in color over x and y, in the form of linear equations
    :param tangent_angle: the angle of the compared to the center of the circle  where the gradient starts
    :return: None
    """
    if tangent_angle == 0:
        tangent_angle = randint(0, 360)
    ce = Geometry.calculate_math_expression
    for i in xrange(radius):
        current_color = (color[0] + int(ce(gradient[0], radius - i)),
                         color[1] + int(ce(gradient[1], radius - i)),
                         color[2] + int(ce(gradient[2], radius - i)))
        circle_center = (int(center[0] + (radius - i) * sin(tangent_angle)),  # x value
                         int(center[1] + (radius - i) * cos(tangent_angle)))  # y value
        cv2.circle(image, circle_center, i, current_color, 2)


def center_gradient_circle(image, center, radius, color=(0, 0, 0), gradient=('2*x', '2*x', '2*x')):
    """
    Action: Draws a circle with a gradient according to the given traits
    :param image: The that the circle should be drawn on, an already open image as a numpy array (opened with cv2.imread)
    :param center: the center of the circle a tuple in the form of (x,y), in pixels, (0,0) is the top left corner
    :param radius: the radius of the circle to be drawn, in pixels
    :param color: the starting color of the circle, in the color space of the image
    :param gradient: the change in color over x and y, in the form of linear equations
    :return: None
    """
    if type(image) == str:
        image = cv2.imread(image)

    ce = Geometry.calculate_math_expression
    for i in xrange(radius):
        current_color = (color[0] + int(ce(gradient[0], radius - i)),
                         color[1] + int(ce(gradient[1], radius - i)),
                         color[2] + int(ce(gradient[2], radius - i)))
        cv2.circle(image, center, i, current_color, 2)


def rotated_rectangle(image, start_point, dimensions, angle=360, color=(0, 0, 0), thickness=1):
    """
    Action: Draws a rotated rectangle
    :param image: The image on which the rectangle should be drawn, a numpy array (an image opened with imread)
    :param start_point: The top left corner, used also as the rotation axis of the rectangle
                        (0, 0) is the top left corner
    :param dimensions: width, height of the rectangle in pixels
    :param color: color of the rectangle in the image's color space
    :param thickness: the thickness of the outline of the rectangle in pixels, -1 means filled
    :param angle: the angle of rotation
    :return: angle of rotation
    """
    if type(image) == str:
        image = cv2.imread(image)
    w, h = dimensions[0], dimensions[1]
    x, y = start_point
    a = [x, y]
    b, d = [x + int(cos(angle) * w), y - int(sin(angle) * w)], [x + int(sin(angle) * h), y + int(cos(angle) * h)]
    vd = [d[0] - x, d[1] - y]
    vb = [b[0] - x, b[1] - y]
    c = [a[0] + vd[0] + vb[0], a[1] + vd[1] + vb[1]]
    pts = array([a, b, c, d], dtype=uint64)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(image, [pts], True, color=color, thickness=thickness)
    return angle


def gradient_rectangle(image, start_point, dimensions, color=(0, 0, 0), grade=-1, angle=360.0,
                       gradient=('2 * x', '2 * x', '2 * x')):
    """
    Action: Draws a rectangle with a changing color
    :param image: image to draw on
    :param start_point: the top left corner of the rectangle from which it is drawn
    :param dimensions: width, height of the rectangle
    :param color: the starting color of the gradient
    :param grade: the starting location of the gradient
    :param angle: optional parameter, the angle of rotation of the rectangle
    :param gradient: the grade of change of the color, it is a tuple of 3 polynomial equations
    (they can be unsimplified) written in python like code as  strings.
    The color space used affects the what each index changes (hsv, bgr, rgb, lab etc)
    the grade according x value is calculated as part of the given equation and then added to the starting value
    so the final value for the first value (regardless of color space) is color[0] + f(x) where f(x) is the result
    of the equation given at the coordinate x.
    Example:
    -----------
    if in the rgb color space:
    ('2 * x', '-3 * x', '2.5 * x')
    increases the red value by 2 for every pixel decreases the green
     value by 3 for every pixel and the blue value by 2.5
    (it is rounded), make sure when using negative values that the corresponding
    starting value is large enough or it will stale at black (or white)
    if in the hsv color space:
    ('0.25 * (x**2) + 2', '(x + 3) / -5', 'x + 3')
    the change in the h value increases by its value squared then multiplied by 0.25 and finally increased by 2
    thus the final h value for every pixel is: starting h value (color[0]) + the result of the
    the s value increases is increased by 3 then divided by -5
    the v value is starting color + 3 + number of pixel (increases by 1 per pixel)
    :return: None
    """
    width, height = dimensions[0], dimensions[1]
    if angle == 360:
        angle = round(uniform(0, 359), 2)
    if grade == -1:
        grade = choice(list_of_grades)

    def draw_straight(point, code):
        x_val, y_val = point[0], point[1]
        ce = Geometry.calculate_math_expression
        if code in [GRADE_N, GRADE_S]:
            for i in xrange(0, height):
                if code is GRADE_N:
                    current_color = (color[0] + int(ce(gradient[0], i)),
                                     color[1] + int(ce(gradient[1], i)),
                                     color[2] + int(ce(gradient[2], i)))
                else:
                    current_color = (color[0] + int(ce(gradient[0], height - i)),
                                     color[1] + int(ce(gradient[1], height - i)),
                                     color[2] + int(ce(gradient[2], height - i)))
                cv2.line(image, (x_val, y_val + i), (x_val + width, y_val + i), color=current_color)
        elif code in [GRADE_W, GRADE_E]:
            for i in xrange(0, width):
                if code is GRADE_W:
                    current_color = (color[0] + int(ce(gradient[0], i)),
                                     color[1] + int(ce(gradient[1], i)),
                                     color[2] + int(ce(gradient[2], i)))
                else:
                    current_color = (color[0] + int(ce(gradient[0], width - i)),
                                     color[1] + int(ce(gradient[1], width - i)),
                                     color[2] + int(ce(gradient[2], width - i)))
                cv2.line(image, (x_val + i, y_val), (x_val + i, y_val + height), color=current_color)
        elif code is GRADE_NW:
            ratio = width / height
            for i in xrange(0, height):
                c_width = int(width - (i * ratio))
                c_height = height - i
                current_color = (color[0] + int(ce(gradient[0], height - i)),
                                 color[1] + int(ce(gradient[1], height - i)),
                                 color[2] + int(ce(gradient[2], height - i)))
                cv2.rectangle(image, start_point, (x_val + c_width, y_val + c_height), current_color, -1)
        elif code is GRADE_NE:
            ratio = width / height
            for i in xrange(0, height):
                c_width = int(width - (i * ratio))
                c_height = height - i
                new_point = (start_point[0] + width, start_point[1])
                x_val, y_val = new_point[0], new_point[1]
                current_color = (color[0] + int(ce(gradient[0], height - i)),
                                 color[1] + int(ce(gradient[1], height - i)),
                                 color[2] + int(ce(gradient[2], height - i)))
                cv2.rectangle(image, new_point, (x_val - c_width, y_val + c_height), current_color, -1)
        elif code is GRADE_SW:
            ratio = width / height
            for i in xrange(0, height):
                c_width = width - int(i * ratio)
                c_height = height - i
                new_point = (start_point[0], start_point[1] + height)
                x_val, y_val = new_point[0], new_point[1]
                current_color = (color[0] + int(ce(gradient[0], height - i)),
                                 color[1] + int(ce(gradient[1], height - i)),
                                 color[2] + int(ce(gradient[2], height - i)))
                cv2.rectangle(image, new_point, (x_val + c_width, y_val - c_height), current_color, -1)
        elif code is GRADE_SE:
            ratio = width / height
            for i in xrange(0, height):
                c_width = width - int(i * ratio)
                c_height = height - i
                new_point = (start_point[0] + width, start_point[1] + height)
                x_val, y_val = new_point[0], new_point[1]
                current_color = (color[0] + int(ce(gradient[0], height - i)),
                                 color[1] + int(ce(gradient[1], height - i)),
                                 color[2] + int(ce(gradient[2], height - i)))
                cv2.rectangle(image, new_point, (x_val - c_width, y_val - c_height), current_color, -1)

    def draw_rotated(point, code):
        ce = Geometry.calculate_math_expression
        if code in [GRADE_N, GRADE_S]:
            for i in xrange(0, height):
                if code is GRADE_N:
                    current_color = (color[0] + int(ce(gradient[0], i)),
                                     color[1] + int(ce(gradient[1], i)),
                                     color[2] + int(ce(gradient[2], i)))
                else:
                    current_color = (color[0] + int(ce(gradient[0], height - i)),
                                     color[1] + int(ce(gradient[1], height - i)),
                                     color[2] + int(ce(gradient[2], height - i)))
                rotated_rectangle(image, point, (width, height - i), color=current_color, thickness=3, angle=angle)
        elif code in [GRADE_W, GRADE_E]:
            for i in xrange(0, width):
                if code is GRADE_W:
                    current_color = (color[0] + int(ce(gradient[0], i)),
                                     color[1] + int(ce(gradient[1], i)),
                                     color[2] + int(ce(gradient[2], i)))
                else:
                    current_color = (color[0] + int(ce(gradient[0], width - i)),
                                     color[1] + int(ce(gradient[1], width - i)),
                                     color[2] + int(ce(gradient[2], width - i)))
                rotated_rectangle(image, point, (width - i, height), color=current_color, thickness=3, angle=angle)
        elif code is GRADE_NW:
            ratio = width / height
            for i in xrange(0, height):
                c_width = int(width - (i * ratio))
                c_height = height - i
                current_color = (color[0] + int(ce(gradient[0], height - i)),
                                 color[1] + int(ce(gradient[1], height - i)),
                                 color[2] + int(ce(gradient[2], height - i)))
                rotated_rectangle(image,
                                  start_point,
                                  (c_width, c_height),
                                  color=current_color,
                                  thickness=3,
                                  angle=angle)
        elif code is GRADE_NE:
            ratio = width / height
            for i in xrange(0, height):
                c_width = int(width - (i * ratio))
                c_height = height - i
                new_point = (start_point[0] + width, start_point[1])
                current_color = (color[0] + int(ce(gradient[0], height - i)),
                                 color[1] + int(ce(gradient[1], height - i)),
                                 color[2] + int(ce(gradient[2], height - i)))
                rotated_rectangle(image,
                                  new_point,
                                  (- c_width, c_height),
                                  color=current_color,
                                  thickness=3,
                                  angle=angle)
        elif code is GRADE_SW:
            ratio = width / height
            for i in xrange(0, height):
                c_width = width - int(i * ratio)
                c_height = height - i
                new_point = (start_point[0], start_point[1] + height)
                current_color = (color[0] + int(ce(gradient[0], height - i)),
                                 color[1] + int(ce(gradient[1], height - i)),
                                 color[2] + int(ce(gradient[2], height - i)))
                rotated_rectangle(image,
                                  new_point,
                                  (c_width, - c_height),
                                  color=current_color,
                                  thickness=3,
                                  angle=angle)
        elif code is GRADE_SE:
            ratio = width / height
            for i in xrange(0, height):
                c_width = width - int(i * ratio)
                c_height = height - i
                new_point = (start_point[0] + width, start_point[1] + height)
                current_color = (color[0] + int(ce(gradient[0], height - i)),
                                 color[1] + int(ce(gradient[1], height - i)),
                                 color[2] + int(ce(gradient[2], height - i)))
                rotated_rectangle(image,
                                  new_point,
                                  (- c_width, - c_height),
                                  color=current_color,
                                  thickness=3,
                                  angle=angle)
    if angle == 0:
        draw_straight(start_point, grade)
    else:
        draw_rotated(start_point, grade)


def white_image(width=320, height=240, color_space=None):
    """
    Action: Creates an image that is completely white
    :param width: Width of the image in pixels, default is 320 pixels
    :param height: Height of the image in pixels, default is 240 pixels
    :param color_space: The color space of the
    :return: The image
    :rtype: numpy array
    """
    img = zeros((height, width, 3), dtype=uint8)
    img[:, :] = (255, 255, 255)
    if color_space is not None:
        return cv2.cvtColor(img, color_space)
    return img


def black_image(width=320, height=240, color_space=None):
    """
    Action: Creates an image that is completely black
    :param width: Width of the image in pixels, default is 320 pixels
    :param height: Height of the image in pixels, default is 240 pixels
    :param color_space: The color space of the
    :return: The image
    :rtype: numpy array
    """
    img = zeros((height, width, 3), dtype=uint8)
    img[:, :] = array([0, 0, 0], dtype=uint8)
    if color_space is not None:
        return cv2.cvtColor(img, color_space)
    return img


def color_image(color, width=320, height=240, color_space=None):
    """
    Action: Creates an image that is completely black
    :param color: The color of the image, in the BGR Color Space
    :param width: Width of the image in pixels, default is 320 pixels
    :param height: Height of the image in pixels, default is 240 pixels
    :param color_space: The color space of the
    :return: The image
    :rtype: numpy array
    """
    img = zeros((height, width, 3), dtype=uint8)
    img[:, :] = color
    if color_space is not None:
        return cv2.cvtColor(img, color_space)
    return img


class GenerateImage:
    """
    An image generating object, give
    """
    def __init__(self, width, height, img_color, true_shape, false_shapes=()):
        """
        Action: Generates random images
        :param width: width of the image in pixels
        :param height: height of the image in pixels
        :param true_shape: the shape object of the true target
        :param false_shapes: a list of the false shapes
        :param img_color:
        """
        self.true = true_shape
        self.false = false_shapes
        self.width, self.height = width, height
        self.image = None
        self.image_color = img_color

    def __random_color(self):
        def random_range(low, high):
            return [randint(low[0], high[0]), randint(low[1], high[1]), randint(low[2], high[2])]

        color_range = self.image_color
        cr_type = type(color_range)
        if cr_type is Color:
            return random_range(color_range.low, color_range.high)
        elif cr_type is MultiColor:
            h, s, v = [], [], []
            for ranges in color_range.ranges:
                j = random_range(ranges.low, color_range.high)
                h.append(j[0])
                s.append(j[1])
                v.append(j[1])
            return [choice(h), choice(s), choice(v)]

    def generate_image(self):
        self.image = color_image(self.__random_color(), self.width, self.height)
        for f in self.false:
            f.draw(self.image, self.width, self.height)
        self.true.draw(self.image, self.width, self.height)
        return self.image


def draw_enclosing_circle(image, contour, color=(0, 0, 0), thickness=1, display_data=True):
    """
    Action: Draws the enclosing (bounding) circle on the given contour
    :param image: image where the contour is, a numpy array or file path
    :param contour: The numpy array describing the shape that should be enclosed by a circle
    :param color: the color of the circle
    :param thickness: the thickness in pixels of the circle
    :param display_data:a bool that determines if the radius of the circle should be displayed
    :return: The image
    :rtype: a numpy array (ndarray)
    """
    def ensure(image_p, rad, cen, inc):
        w, h, _ = image_p.shape
        o1 = int(cen[1] - rad - 1.5 * inc)
        o2 = int(cen[1] + rad + 1.5 * inc)
        o3 = int(cen[0] - rad - 1.5 * inc)
        o4 = int(cen[0] + rad + 1.5 * inc)
        if o1 >= 0:
            return cen[0], o1
        elif o2 <= h:
            return cen[0], o2
        elif o3 >= 0:
            return o3, cen[1]
        elif o4 <= w:
            return o4, cen[1]

    if type(image) is str:
        image = cv2.imread(image)
        if image is None:
            raise ValueError('Given image is an invalid path (check if the image path exists)'
                             ' and image could not be opened.')
    center, radius = cv2.minEnclosingCircle(contour)
    c = (int(center[0]), int(center[1]))
    r = int(radius)
    cv2.circle(image, c, r, color, int(thickness))
    if display_data:
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        c = ensure(image, r, c, 5)
        cv2.putText(image, str(r), c, font, 0.5, color, 2)
    return image


def draw_bounding_rect(image, contour, color=(0, 0, 0), thickness=1, display_data=True):
    """
    Action: draws the straight bounding rectangle around the given contour.
    :param image: Image where the contour is, a numpy array or file path to the image
    :param contour: The numpy array describing the shape that should be bounded by a rectangle
    :param color: color of the outline of the bounding rectangle, bgr color space
    :param thickness: thickness of the bounding rectangle in pixels, -1 fills the shape
    :param display_data: a bool that determines if the
    :return: the image
    :rtype: a numpy array (ndarray)
    """
    if type(image) is str:
        image = cv2.imread(image)
        if image is None:
            raise ValueError('Given image is an invalid path (check if the image path exists)'
                             ' and image could not be opened.')

    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), color=color, thickness=thickness)
    if display_data:
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        text = 'w=' + str(w) + ', h=' + str(h)
        cv2.putText(image, text, (x, y - 5), font, 0.75, color, 2)
    return image
