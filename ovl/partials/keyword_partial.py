import functools
import warnings

from .reverse_partial import ReversePartial


def keyword_partial(target_function):
    """
    A Decorator used to load other parameters to a function before applying it on a given input data
    This decorator is used to load parameters to the filter function, image processing filters, morphological functions
    sorters and other functions that act similarly.

    Preloading a function consists of pass all arguments except the first,
    which is then passed when the function is called.

    Example:

    For a given function:

    .. code-block:: python

        @keyword_partial
        def area_filter(contours, min_area, max_area):
            output_list = []
            ratio_list = []
            if type(contour_list) is not list:
                contour_list = [contour_list]
            for current_contour in contour_list:
                if min_area <= cv2.contourArea(current_contour) <= max_area:
                    output_list.append(current_contour)
                    ratio_list.append(current_contour)
            return output_list, ratio_list


    Instead of calling the function like other functions:

    .. code-block:: python

        area_filter(list_of_contours, min_area=200, max_area=5000)

    The function needs to be called as follows:

    .. code-block:: python

        activator = area_filter(min_area=200, max_area=5000)

        final_value = activator(list_of_contours)


    Vision objects use functions that are decorated with keyword_partial (contour_filter, image_filter,
    you can just pass the activator to the Vision object like so:

    .. code-block:: python

       target_filters = [some_filter(parameter1=5, parameter2=3), ovl.circle_filter(min_area_ratio=0.75)]

       vision = Vision(...,  contours_filters=target_filters, ...)

    :param target_function: the function to be preloaded
    :return: a function (argument loader) that preloads (passes only some of the arguments)
             the wrapped function (target_function)
    """
    def argument_loader(*args, **kwargs):
        if args != ():
            warning_message = ("When passing parameters it is recommended to pass everything as keywords "
                               "in order to make it clear what parameters are passed."
                               "(Do: {0}(parameter1=value2, parameter2=value2) not {0}(value, value2))"
                               .format(target_function.__name__))
            warnings.warn(warning_message, SyntaxWarning)
        partial_function = ReversePartial(target_function, *args, **kwargs)
        return functools.update_wrapper(partial_function, target_function)

    wrapped_argument_loader = functools.update_wrapper(argument_loader, target_function)
    return wrapped_argument_loader

