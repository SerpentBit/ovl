from ..partials.keyword_partial import keyword_partial


TARGET_FILTERS = set()


def target_filter(target_filter_function):
    """
    A decorator function used to make a contour filter function.
    Target filters are functions that take a list of targets
    and returns only


    Wrapping a function it gives the following capabilities:
        - pass parameters before the list of targets
        - preserves the properties of the function: name, documentation etc.

    The `target_filter` then changes it behaviour to act as follows:


    For a given function:


    .. code-block:: python

        @target_filter
        def area_filter(contours, min_area, max_area):
            output_list = []

            for current_contour in contour_list:
                if min_area <= cv2.contourArea(current_contour) <= max_area:
                    output_list.append(current_contour)
            return output_list



    Instead of calling the function like other functions:

    .. code-block:: python

        some_filter(list_of_contours, 200, 5000)

    The function needs to be called as follows:

    .. code-block:: python

         activator = area_filter(200, 5000)

         result = activator(list_of_contours)


    Vision objects use functions that are decorated with target_filter
    you can just pass the activator to the Vision object
    like so:

     .. code-block:: python

        target_filters = [area(min_area=400, max_area=5000), ovl.circle_filter(min_area_ratio=0.75)]

        vision = Vision(..., target_filters=target_filters, ...)
    """
    TARGET_FILTERS.add(target_filter_function)
    return keyword_partial(target_filter_function)
