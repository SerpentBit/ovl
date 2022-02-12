from ..partials.keyword_partial import keyword_partial

IMAGE_FILTERS = set()


def image_filter(image_filter_function):
    """
    A decorator used to pass parameters in two stages,
    run in a python console `help(ovl.target_filter)`
    or look at ovl.target_filter documentation for more information
    image_filter acts like target_filter except it receives an image (np.ndarray)
    applies changes on it and then returns it altered.
    functions decorated by image_filter can be passed to Vision(image_filters_)

    Changes that are applied can vary from  blurs, image rotations, translations, contrast and brightness alterations
    and color spaces conversions (HSV, RGB Greyscale conversions)

    Filters that change binary images (images that have been threshold by
    a threshold object such as ovl.Color ovl.MultiColor or ovl.Canny) like morphological
    functions (ex. erosion, dilation) count as image filters as well and should be
    decorated using image_filter.

    image filter example:

    .. code-block:: python

        @image_filter
        def rotate_by_angle(image, angle):
            (height, width) = image.shape[:2]
            center_xy = (width / 2, height / 2)
            rotation_matrix = cv2.getRotationMatrix2D(center_xy, -angle, 1.0)
            cos = np.abs(rotation_matrix[0, 0])
            sin = np.abs(rotation_matrix[0, 1])
            rotated_image_dimensions = (int((height * sin) + (width * cos)), int((height * cos) + (width * sin)))
            rotation_matrix[0, 2] += (rotated_image_dimensions[0] / 2) - center_xy[0]
            rotation_matrix[1, 2] += (rotated_image_dimensions[1] / 2) - center_xy[1]
            return cv2.warpAffine(image, rotation_matrix, rotated_image_dimensions)

    The filter can then be passed to a Vision object to be applied to the images
    in the pipeline.


    .. code-block:: python

        pipeline = Vision(image_filters=[rotate_by_angle(angle=180)]
    """
    filter_partial = keyword_partial(image_filter_function)
    IMAGE_FILTERS.add(filter_partial)
    return filter_partial
