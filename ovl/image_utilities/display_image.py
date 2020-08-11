from typing import List, Union

import cv2
from numpy import vstack, hstack, ndarray

WINDOWS = []


def stitch_images(images):
    width, height = images[0].shape
    stitched_image = cv2.imread(images[0]) if type(images[0]) is str else images[0]
    for image in images[1:]:
        if type(image) is str:
            image = cv2.imread(image)
        image_shape = image.shape
        if width + image_shape[0] > height + image_shape[1]:
            stitched_image = vstack((stitched_image, image))
            width += image_shape[0]
        else:
            stitched_image = hstack((stitched_image, image))
            height += image_shape[1]
    return stitched_image


def show_image(image, window_name, delay):
    cv2.imshow(window_name, image)
    return cv2.waitKey(delay)


def display_image(image: Union[ndarray, str, List[ndarray, str]], window_name='image', display_loop=False,
                  resizable=False):
    """
    The function displays an image

    The function is based on cv2.imread()
    is able to open both paths and numpy arrays (already opened) images

    When using this function to display images in a loop, delay=0 will cause the loop to stop until
    a key is pressed.

    .. code-block:: python

        for frame in video_frames:
            ovl.display_image(frame, delay=1)
            # the video will play normally in one window

    If delay is 0:

    .. code-block:: python

        for frame in video_frames:
            ovl.display_image(frame)
            # the video will freeze until a key is pressed



    :param image: Represents an image path (string), an already open image in the for of a numpy array (ndarray)
                  or a list of images (strings and arrays are valid)
    :param window_name: Name of the Window that displays the images
    :param display_loop: if display is used in a loop should be true, else false
    :param resizable: A boolean that determines whether the image window is resizable or not
    :return: the key pressed while image was displayed
    """
    if isinstance(image, str):
        image = cv2.imread(image)
    elif isinstance(image, list):
        image = stitch_images(image)
    elif not isinstance(image, ndarray):
        raise TypeError("Invalid image given, image must be an image, a path to an image or a list of images")

    if resizable:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    return show_image(image, window_name, display_loop * 1)
