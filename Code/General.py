# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
from math import pi
from time import sleep, gmtime, strftime
from sys import version_info
from json import dumps, loads


if version_info[0] == 3:
    xrange = range


def print_pipe(out, *args):
    """
    Action: outputs the given args to the output given, screen, file or not at all.
    :param out: the output location None to screen False doesnt print a path is saved to a file
    :param args: the data to be printed
    :return: None
    """
    if out is False:
        pass
    elif out is None:
        for i in args:
            print(str(i))
        print('')
    else:
        with open(out, 'a') as f:
            print(args)
            text = strftime("%a, %d %b %Y %H:%M:%S:: ", gmtime()) + str(args)
            f.write(text)
            f.close()


class ToolClass:
    help_text = "The help and documentation text for %s hasn't been defined"

    @property
    def help(self):
        return self.__class__.help_text.replace('%s', self.__class__.__name__)

    def __init__(self):
        print('')
        print_pipe(None, self.help)
        sleep(0.25)
        raise ToolError("Tool classes cannot be instantiated ")


class TimeQueue:
    def __init__(self, capacity):
        self.time = []
        self.value = []
        self.capacity = capacity

    def push(self, value, time):
        """
        Action:
        :param value:
        :param time:
        :return:
        """
        self.time.append(time)
        self.value.append(value)
        if len(time) >= self.capacity:
            self.deque()

    def deque(self):
        """
        Action: removes the oldest time and value
        :return:
        """
        del self.time[0]
        del self.value[0]

    def get_value_at_time(self, time):
        """
        Action:Gets the value closest to a given time stamp
        :param time:
        :return:
        """
        return self.time[min(enumerate(self.time), key=lambda i: abs(self.time[i] - time))[1]]


class InvalidCustomError(Exception):
    pass


class TimeTracker:

    def __init__(self, name):
        self.name = name
        self.__times = []

    @property
    def length(self):
        return len(self.__times)

    def add_time(self, value):
        if type(value) in [float, int]:
            self.__times.append(value)

    def get_average(self):
        """
        Action: calculates the average of the times.
        :return: the float representing the average
        """
        return sum(self.__times) / float(len(self.__times))

    def get_sum_of_squares(self):
        """
        Action: Calculates the sum of square deviations of the times.
        :return: float
        """
        return sum((x - self.get_average()) ** 2 for x in self.__times)

    def get_standard_deviation(self, dof=0):
        """
        Action: returns the
        :param dof: degrees of freedom, 0 population sd, 1 for sample mean
        :return:
        """
        length = self.length
        if length < 2:
            raise ValueError('Variance requires at least 2 times.')
        population_var = self.get_sum_of_squares() / (length - dof)
        return root(population_var)

    def sd(self, dof=0):
        return self.get_standard_deviation(dof)

    def avg(self):
        return self.get_average()

    def serialize(self):
        f = {'times': self.__times, 'name': self.name}
        return dumps(f)

    def pack(self, path):
        with open(path, 'w') as f:
            f.write(self.serialize())
            f.close()


class Performance:
    def __init__(self, names):
        self.trackers = {}
        for name in names:
            self.trackers[name] = TimeTracker(name)

    def add(self, name, value):
        self.trackers[name].add_time(value)

    def get_averages(self):
        return [i.avg() for i in self.trackers]


class VersionError(Exception):
    pass


class ToolError(Exception):
    pass


def root(base, degree=2):
    """
    Action: Raises base to the root of degree. [base^(1/degree)]
    :param base: The number to be raised
    :param degree: The root
    :return: the result
    :rtype: Float
    """
    return float(base) ** (1 / float(degree))


def get_calibrated_value(img_mean, vector):
    """
    Action: Solves the calibration equation that finds the optimal low bound value for
            the saturation and value.
    :param img_mean: the mean if the image of which
    :param vector: the dictionary containing the coefficients and group mean.
    :return: the optimal low bound
    """
    data_mean = vector['mean'][0]
    z_mean = data_mean[0] * vector['co1'] + data_mean[1] * vector['co2']
    return (z_mean - (img_mean * vector['co1'])) / vector['co2']


def radians2degrees(radians):
    """
        :param radians: the radians to be converted
        :return: returns the degrees equivalent of the given degrees
        """
    return radians * 180 / pi


def degrees2radians(degrees):
    """
    :param degrees: the degrees to be converted
    :return: returns the radian equivalent of the given degrees
    """
    return degrees * pi / 180


def numerical_replace(string, *args):
    for i in xrange(len(args)):
        string = string.replace(str(i), str(i) + '!%$#*^&#@^#%')

    for number, replacement in enumerate(args):
        string = string.replace(str(number) + '!%$#*^&#@^#%', str(replacement))
    return string


def enumertype(iterable):
    for obj in iterable:
        yield type(obj), obj
