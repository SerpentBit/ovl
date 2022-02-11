from typing import List
import numpy as np
import functools

from ..partials.reverse_partial import ReversePartial


def _loaded_condition(loaded_contour_filter, contour_list: List[np.ndarray]):
    return list(filter(loaded_contour_filter, contour_list))


def single_target_filter(single_contour_filter):
    """
    A target_filter that turns a function that filters a single contour (and returns true if it has passed)
    to an iterative one that goes over a list

    example:

    .. code-block:: python

        @single_target_filter
        def area_filter(contour, minimum_area=50)
            return cv2.contourArea(contour) > minimum_area

    This function can then be passed to a Vision object:

    .. code-block:: python

        filters = [area_filter(min_area=60)] # sets the minimum area to 60 -> the first parameter passed
        vision = Vision(..., target_filters=filters, ...)

    :param single_contour_filter: the function to turn into a contour filter, which loads the parameters to the filter
    before running it on list of contour filters.
    :return: the argument loader that wraps the target function
    """

    def argument_loader(*args, **kwargs):
        condition = ReversePartial(single_contour_filter, *args, **kwargs)
        argument_loader.condition = condition
        return functools.partial(_loaded_condition, condition)
    return argument_loader
