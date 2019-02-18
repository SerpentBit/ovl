# Copyright 2018 - 2019 Ori Ben-Moshe - All rights reserved.
from .General import root, radians2degrees, degrees2radians
import cv2
from math import pi, cos as cosinus, sin as sinus, log, tan as tangent, factorial, atan as arctan
from sys import version_info
import numpy as np


def atan(x):
    """
    Action: Arc tangent in degrees
    :param x: the tangent
    :return: the angle in degrees
    """
    return radians2degrees(arctan(x))


def y_intersection(line_slope, intercept, x_val):
    """
    Action: finds the y value of the line (y = mx + b) at point x
    :param line_slope: slope of the line (m)
    :param intercept: the intercept of the line (b)
    :param x_val: the value to be used (substituted with x)
    :return: the y value
    """
    return x_val, line_slope * x_val + intercept


def x_intersection(line_slope, intercept, y_val):
    """
    Action: calculates the x value of which the line according to the given y value
    :param line_slope:
    :param intercept:
    :param y_val:
    :return:
    """
    return (y_val - intercept) / float(line_slope), y_val if line_slope != 0 else (0, y_val)


def distance_from_frame(point, image_dimensions):
    """
    Action calculates the distance of a given point for the frame of the image based on the vector from the center
    and the point
    :param point: point (x,y tuple) or contour (ndarray)
    :param image_dimensions: the size of the image, (width, height)
    :return: the distance
    """
    p = get_contour_center(point) if type(point) is np.ndarray else point
    image_center = (image_dimensions[0] / 2 - .5, image_dimensions[1] / 2 - .5)
    s = slope(point, image_center)
    i = - s * p[0] + p[1]
    xs = (image_dimensions[0] - 1, 0)
    ys = (image_dimensions[1] - 1, 0)
    x_inter = x_intersection
    y_inter = y_intersection
    dbp = distance_between_points
    return min([dbp(x_inter(s, i, x), p) for x in xs] + [dbp(y_inter(s, i, y), p) for y in ys])


def horizon_angle(point, field_of_view, image_width):
    """
    Action: returns the angle compared to the center of the image for a given field of view image width and point
    :param point: the x val or center
    :param field_of_view: the horizontal field of view
    :param image_width: the image width
    :return: the angle compared to the center of the image , negative left positive right.
    """
    x_val = point[0] if type(point) in (tuple, list, set) else point
    return float(atan((x_val - (image_width - 1) / 2) / float(focal_length(image_width, field_of_view))))


def vertical_angle(point, field_of_view, image_height):
    """
    Action: returns the angle compared to the center of the image for a given field of view image height and point
    :param point: the x val or center
    :param field_of_view: the vertical field of view
    :param image_height: the image height
    :return: the angle compared to the center of the image , negative up positive down6.
    """
    y_val = point[1] if type(point) in (tuple, list, set) else point
    return float(atan((y_val - (image_height - 1) / 2) / float(focal_length(image_height, field_of_view))))


def focal_length(image_width, field_of_view):
    """
    Action: calculates the focal length given an image width and field of view
    :param image_width:
    :param field_of_view:
    :return: calculates the focal length, a float
    """
    return image_width / float((2 * tan(float(field_of_view / 2))))


def open_arc_length(contour):
    """
    Action: Returns the arc length of an "open" contour
    :param contour:
    :return:
    """
    return cv2.arcLength(contour, False)


def slope(p1, p2):
    """
    Action: returns the slope between 2 points
    :param p1: first point (x,y)
    :param p2: second point (x,y)
    :return: the slope
    """
    return  0. if p1[0] == p2[0] else ((float(p1[1]) - float(p2[1])) / (float(p1[0]) - float(p2[0])))


def angle_between_points(p1, p2):
    """
    Action: calculates the angle between the 2 points and the horizontal axis
    :param p1: the first point (2d)
    :param p2: the second point  (2d)
    :return: the angle
    """
    return radians2degrees(atan(slope(p1, p2)))


def line_angle(contour):
    """
    Action: returns the angle of the line created by the top-most and
    bottom-most points of a contour
    :param contour: the contour, a numpy array
    :return: the angle in degrees
    """
    if type(contour) != np.ndarray:
        raise TypeError("Contour must be a numpy array")
    topmost = tuple(contour[contour[:, :, 1].argmin()][0])
    bottommost = tuple(contour[contour[:, :, 1].argmax()][0])
    return angle_between_points(topmost, bottommost)


def get_approximation_open(contour, approximation_coefficient=0.02):
    """
    Action: returns the vertices of the approximation of the contour
    NOTE: for "open" contours!
    :param contour: open contour (ndarray)
    :param approximation_coefficient: approximation coefficient
    :return: list of vertices
    """
    arc = approximation_coefficient * cv2.arcLength(contour, False)
    return cv2.approxPolyDP(contour, arc, False)


def sin(x):
    """
    Action: The trigonometric function, sine.
    :param x: an angle in degrees
    :return: result, float
    """
    return sinus(degrees2radians(x))


def cos(x):
    """
    Action:  The trigonometric function, cosine.
    :param x: an angle in degrees
    :return: result, float
    """
    return cosinus(degrees2radians(x))


def tan(x):
    """
    Action: The trigonometric function, tangent.
    :param x: an angle in degrees
    :return: result, float
    """
    return tangent(degrees2radians(x))


math_funcs = {'sin': sin, 'cos': cos, 'tan': tan, 'fact': factorial, 'log': log}


def calculate_math_expression(equation, value, additional_functions=None, symbol='x'):
    """
    Action: calculates a math expression with a
    :param equation:
    :param value:
    :param additional_functions:
    :param symbol: The symbol in the equation
    :return:
    """
    expression = equation.replace(symbol, str(value))
    if additional_functions is None:
        additional_functions = math_funcs

    if version_info[0] == 3:
        exec('equation_res = ' + expression, additional_functions)
        return locals()['equation_res']
    else:
        locals().update(math_funcs)
        equation_res = 0
        exec('equation_res = ' + expression)
        return locals()['equation_res']


def get_circle_area(radius):
    """
    Action: calculates the area of a circle with the given radius.
    :param radius: The radius of the circle
    :return: Area of the circle
    """
    return pi * (radius ** 2)


def distance_between_points(p1, p2):
    """
    Action: Calculates the Distance between 2 points.
    :param p1: tuple of x and y value of point 1
    :param p2: tuple of x and y value of point 2
    :return: Float value of the distance between the 2 points
    :rtype: float
    """
    return root((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2, 2)


def get_fill_ratio_straight(contour, reverse_div=False):
    """
    Action: Returns the ratio between the contour and the straight bounding rectangle.
    :param contour: The contour to be compared
    :param reverse_div: If the rectangle's area should be divided by the contour.
    :return:  the ratio, the width of the bounding rectangle, the height of the bounding rectangle
    :rtype: float
    """
    _, _, w, h = cv2.boundingRect(contour)
    r_area = w * h
    c_area = cv2.contourArea(contour)
    if reverse_div:
        return float(r_area) / c_area, w, h
    return float(c_area) / r_area, w, h


def get_fill_ratio_triangle(contour, triangle=None, reverse_div=False):
    """
    Action: returns the ratio
    :param contour:
    :param triangle: convex hull for the minEnclosingTriangle function, can be ignored
    :param reverse_div: If the triangle's area should be divided by the contour.
    :return:
    """
    t_area, t = cv2.minEnclosingTriangle(contour, triangle)
    c_area = cv2.contourArea(contour)
    if reverse_div:
        return float(t_area) / c_area
    return c_area / float(t_area)


def get_fill_ratio_rotating(contour, reverse_div=False):
    """
    Action: Returns the ratio between the contour and the smallest bounding rectangle.
    :param contour: The contour to be compared
    :param reverse_div: If the Rectangle should be divided by the contour.
    :return: the ratio, the width of the bounding rectangle, the height of the bounding rectangle
    :rtype: float
    """
    rotated = cv2.minAreaRect(contour)
    r_area = rotated[1][0] * rotated[1][1]
    c_area = cv2.contourArea(contour)
    if reverse_div:
        return float(r_area) / c_area, rotated[1][0], rotated[1][1]
    return float(c_area) / r_area, rotated[1][0], rotated[1][1]


def get_fill_ratio_circle(contour, reverse_div=False):
    """
    Action: Returns the ratio between the contour and the smallest enclosing circle.
    :param contour: The contour to be compared
    :param reverse_div: If the circle should be divided by the contour.
    :return: the ratio, the radius of the enclosing circle
    :rtype: float
    """
    _, enclosing_radius = cv2.minEnclosingCircle(contour)
    circle_area = get_circle_area(enclosing_radius)
    contour_area = cv2.contourArea(contour)
    if reverse_div:
        return float(circle_area) / contour_area, enclosing_radius
    return float(contour_area) / circle_area, enclosing_radius


def get_contour_center(contour):
    """
    Action: Returns the coordinates center of a contour
    :param contour: a single contour
    :return: X coordinate of center, Y coordinate of center
    :rtype: int, int
    """
    moments = cv2.moments(contour)
    try:
        x, y = int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])
    except ZeroDivisionError:
        raise ValueError('Contour given is too small!')
    return x, y


def n_polygon_angle(amount_of_sides):
    """
    Action: returns the inner angle of a polygon with the given amount of sides
    :param amount_of_sides: amount of sides the polygon has
    :return:
    """
    n = amount_of_sides
    return (n - 2) * (180 / n)


def get_approximation(contour, approximation_coef=0.02):
    """
    Action: returns the approximation
    :param contour:
    :param approximation_coef:
    :return:
    """
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, approximation_coef * peri, True)
    return approx


def n_polygon_area(length, amount_of_sides):
    """
    Action: area of a polygon of
    :param length:
    :param amount_of_sides:
    :return:
    """
    angle = 180 / amount_of_sides
    return 0.25 * amount_of_sides * (length ** 2) * (cos(angle)/sin(angle))


def circle_rating(contour, area_factor=0.9, radius_factor=0.8):
    """
    Action: returns a rating of how close is the circle to being a circle
    :param contour: the contour that its rating is calculated
    :param area_factor: the factor (p-value) that separates an area ratio that is a circle and one that isn't
    :param radius_factor: the factor (p-value) that separates an radius ratio that is a circle and one that isn't
    :return:
    """
    fill_ratio, radius = get_fill_ratio_circle(contour)
    _, _, w, h = cv2.boundingRect(contour)
    radius_ratio = root(((radius * 2) ** 2) / float(w) * h, 2)
    rating = (radius_ratio * radius_factor) * (fill_ratio * area_factor)
    return rating


def get_lengths_and_angles(contour, approximation_coefficient=0.02):
    """
    Action: returns a list of lengths and angles of a given contour.
    :param contour: contour (numpy array) to find its
    :param approximation_coefficient:
    :return: returns the list of sides
    """
    def cosine_sentence(p1, p2, p3):
        dbp = distance_between_points
        l1, l2, l3 = dbp(p1, p2), dbp(p1, p3), dbp(p2, p3)
        alpha = (l1**2 + l2**2 - l3**2) / (l1 * l2 * 2)
        return radians2degrees(alpha)

    approximation = get_approximation(contour, approximation_coefficient)
    vertices = []
    lengths = []
    angles = []
    for points in approximation:
        vertex = points[0][1], points[0][0]
        vertices.append(vertex)

    for idx, point in enumerate(vertices):
        if idx == len(approximation) - 1:
            lengths.append(distance_between_points(point, vertices[0]))
            angles.append(cosine_sentence(vertices[idx - 1], point, vertices[0]))
        else:
            lengths.append(distance_between_points(point, vertices[idx + 1]))
            angles.append(cosine_sentence(vertices[idx - 1], point, vertices[idx + 1]))
    return vertices, lengths, angles
