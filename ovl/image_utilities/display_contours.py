import copy
import math

from .display_image import *
from ..image_utilities.open_image import open_image


def display_contours(image, contours, amount=0, display_loop=False, window_name="image", color=(0, 255, 0),
                     save_path=None):
    """
    Displays the image with the current_vision list of contours

    This can be used to display detected contours (object outlines) on an image (numpy array)

    .. code-block:: python

        import ovl
        import cv2

        image = cv2.imread("path/to/image.png")

        (define a vision pipeline to detect contours)

        contours, _ = vision.detect(image)

        ovl.display_contours(image, contours)


    :param image: image from which the contours were taken from, numpy array or image path
    :param contours: the list of contours to display_image
    :param color: the color of the of the contours outline
    :param display_loop: if display is used in a loop should be true, else false
    :param window_name: the window name, this is useful when display multiple different images at the same time
    :param amount: amount of contours to display
    :param save_path: if the image should be saved, pass the wanted result path
    :return: the image with the drawn contours.
    """
    if type(image) is str:
        image = open_image(image)
    image_for_display = copy.copy(image)
    if amount == math.inf:
        amount = 0
    contours = contours[0:amount] if amount > 0 else contours
    cv2.drawContours(image_for_display, contours, -1, color, 2)
    if type(save_path) is str:
        cv2.imwrite(save_path, image_for_display)
    display_image(image_for_display, window_name=window_name, display_loop=display_loop)
    return image_for_display
