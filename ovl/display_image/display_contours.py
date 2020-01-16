import copy

from .display_image import *


def display_contours(image, contours, amount=0, delay=None, color=None, save_path=None):
    """
     Displays the image with the current_vision list of contours
    :param image: image from which the contours were taken from, numpy array or image path
    :param contours: the list of contours to display_image
    :param color: the color of the of the contours outline
    :param delay: delay for the wait key function, None means wait indefinitely,
                  add a delay when using this function in loops
    :param amount: amount of contours to display_image
    :param save_path: if the image should be saved, pass the wanted result path
    :return: the image with the drawn contours.
    """
    if type(image) is str:
        image = cv2.imread(image)
    image_for_display = copy.copy(image)
    contours = contours[0:amount] if amount > 0 else contours
    if color is None:
        color = (0, 0, 0)
    cv2.drawContours(image_for_display, contours, -1, color, 2)
    if type(save_path) is str:
        cv2.imwrite(save_path, image_for_display)
    display_image(image_for_display, delay=delay)
    return image_for_display
