import cv2

from ..helpers.remove_none_values import remove_none_values


def open_image(image_path, flags=None):
    """
    Opens an image file, has a more direct error detection to find out problems
    that occurred during image opening, has a cost in performance.
    
    :param image_path: the path of the image to open
    :param flags: there are multiple flags that can be used to alter how the image is loaded
     https://docs.opencv.org/4.3.0/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56
    :return: the opened image or a iterator that opens the list of images given
    """
    arguments = {"flags": flags}
    image = cv2.imread(image_path, **remove_none_values(arguments))
    if image is None:
        raise ValueError("Couldn't read the image file, Check that {}\n"
                         "exists, that it's a valid format and that you\n"
                         "have the proper permissions to read it.".format(image))
    return image
