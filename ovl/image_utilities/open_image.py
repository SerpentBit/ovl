import cv2
from pathlib import Path


def open_image(image_path, flags=None):
    """
    Opens an image file, has a more direct error detection to find out problems
    that occurred during image opening, has a cost in performance.
    
    :param image_path: the path of the image to open
    :param flags: there are multiple flags that can be used to alter how the image is loaded
     https://docs.opencv.org/4.3.0/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56
    :return: the opened image or an iterator that opens the list of images given
    """
    if not Path(image_path).is_file():
        raise OSError(f"Given image at path {image_path} does not exist or is not a file!")

    image = cv2.imread(image_path, flags=flags)
    if image is None:
        raise ValueError(f"Failed to read the image file, Check that {image} exists, that it's a valid format and that "
                         f"you have the proper permissions to read it.")
    return image
