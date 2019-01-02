# Copyright 2018 Ori Ben-Moshe - All rights reserved.
from General import root, radians2degrees, degrees2radians
import cv2
from math import pi, cos as cosinus, sin as sinus, log, tan as tangent, factorial, acos
from sys import version_info


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

