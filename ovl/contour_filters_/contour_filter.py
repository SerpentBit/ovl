from ..partials import keyword_partial


CONTOUR_FILTERS = set()


def contour_filter(contour_filter_function):
    """
    A decorator function used to make a contour filter function.
    Contours filters are functions that take a list of contours
    and returns only


    Wrapping a function it gives the following capabilities:
        - pass parameters before the list of contours
        - preserves the properties of the function: name, documentation etc.

    The contours filter then changes it behaviour to act as follows:


    For a given function:

        @contour_filter
        def area_filter(contours, min_area, max_area):
            output_list = []
            ratio_list = []

            for current_contour in contour_list:
                if min_area <= cv2.contourArea(current_contour) <= max_area:
                    output_list.append(current_contour)
                    ratio_list.append(current_contour)
            return output_list, ratio_list


    Instead of calling the function like other functions:

        A1| some_filter(list_of_contours, 200, 5000)

    The function needs to be called as follows:

        B1| activator = area_filter(200, 5000)
        B2|
        B3| result = activator(list_of_contours)


    Vision objects use functions that are decorated with contour_filter
    you can just pass the result of line B1 to the Vision object
    like so:

        C1| contour_filters = [area(400, 5000), ovl.circle_filter(0.75)]
        C2|
        C3| vision = Vision(..., contour_filters=contour_filters, ...)
    """
    CONTOUR_FILTERS.add(contour_filter_function)
    return keyword_partial.keyword_partial(contour_filter_function)
