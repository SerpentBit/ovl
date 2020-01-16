from ..partials.keyword_partial import keyword_partial


def image_filter(image_filter_function):
    """
    A decorator used to pass parameters in two stages,
    run in a python console "help(ovl.contour_filter)" or ovl.contour_filter.__doc__
    or look at ovl.contour_filter documentation for more information
    image_filter acts like contour_filter except it receives an image (np.ndarray)
    applies changes on it and then returns it altered.
    functions decorated by image_filter can be passed to Vision(image_filters_)

    Changes that can be applied vary from various blurs like Gaussian blur or Bilateral filter to image rotations
    translations, contrast and brightness alterations and color spaces changes (HSV, RGB Greyscale conversions)

    Filters that change binary images (images that have been threshold by
    a threshold object such as ovl.Color ovl.MultiColor or ovl.Canny) like morphological
    functions (ex. erosion, dilation) count as image filters as well and should be
    decorated using image_filter.

    image filter example:
        1 |    @image_filter
        2 |    def rotate_by_angle(image, angle):
        3 |        (height, width) = image.shape[:2]
        4 |        center_xy = (width / 2, height / 2)
        5 |        rotation_matrix = cv2.getRotationMatrix2D(center_xy, -angle, 1.0)
        6 |        cos = np.abs(rotation_matrix[0, 0])
        7 |        sin = np.abs(rotation_matrix[0, 1])
        8 |        rotated_image_dimensions = (int((height * sin) + (width * cos)), int((height * cos) + (width * sin)))
        9 |        rotation_matrix[0, 2] += (rotated_image_dimensions[0] / 2) - center_xy[0]
        10|        rotation_matrix[1, 2] += (rotated_image_dimensions[1] / 2) - center_xy[1]
        11|        return cv2.warpAffine(image, rotation_matrix, rotated_image_dimensions)
    """
    return keyword_partial(image_filter_function)
