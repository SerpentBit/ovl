import cv2

from .naming_conventions import *


def photo_array(camera, amount, delay=3, name_convention=time_name_convention, path=None):
    """
    Takes a series of images with a delay between shots and saves them, after every image,
    press 'y' to save it and 'n' to pass

    :param camera: the camera to take images with, ovl.Camera or cv2.VideoCapture
    :param amount: the amount of images to take, must be a positive integer
    :param delay: the delay between images
    :param name_convention: the naming convention of the images
    :param path: if images should be saved in a specific folder
    :return: the images
    """
    images = []
    for image_number in range(amount):
        ret, image = camera.read()
        if ret:
            images.append(image)
            save_name = name_convention(image_number)
            save_name = path + save_name if path else save_name
            while True:
                cv2.imshow('Ovl Photo Array', image)
                key = cv2.waitKey(delay)
                if key == ord('y'):
                    cv2.imwrite(save_name, image)
                    break
                elif key == ord('n'):
                    break
    return images
