from typing import Tuple

import cv2
import numpy as np

from .image_filter import image_filter
from ..utils.remove_none_values import remove_none_values
from .kernels import validate_odd_size
from ..utils.types import RangedNumber
from ..utils.constants import DEFAULT_KERNEL_SIZE


def convert_to_hsv(image: np.ndarray) -> np.ndarray:
    """
    Converts an image to hsv - Mainly for beginner use
    
    :param image: image to be converted
    :return: the converted image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


@image_filter
def sharpen_image(image: np.ndarray, size: tuple = DEFAULT_KERNEL_SIZE) -> np.ndarray:
    """
    Sharpens an image by preforming convolution it with a sharpening matrix

    :param image: the image (numpy array)
    :param size: the size of the sharpening matrix
    :return: the new sharpened image
    """

    validate_odd_size(size)
    kernel = np.ones(size)
    kernel *= -1
    kernel[int((size[0] - 1) / 2), int((size[1] - 1) / 2)] = kernel.size
    return cv2.filter2D(image, -1, kernel)


@image_filter
def adaptive_brightness(image: np.ndarray, brightness: RangedNumber(0, 100) = 50, hsv: bool = False) -> np.ndarray:
    """
    Changes the brightness of every pixel so that the polygon_filter_average of the image is the target polygon_filter_average

    :param image: The image to be changed (Numpy array)
    :param brightness: the target polygon_filter_average for the image
    :param hsv: bool noting if the image is in hsv
    :return: a copy of the image changed
    """
    image = image if hsv else cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    brightness = brightness * 2.55
    image_hue_mean = cv2.mean(image)[2]
    increase = brightness - image_hue_mean
    vid = image[:, :, 2]
    if increase > 0:
        vid = np.where(vid + increase <= 255, vid + increase, 255)
    else:
        vid = np.where(vid + increase >= 0, vid + increase, 0)
    image[:, :, 2] = vid
    image = image if hsv else cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image


@image_filter
def change_brightness(image: np.ndarray, change: float = 25, hsv_image: bool = False) -> np.ndarray:
    """
    Changes the brightness of every pixel of a BGR image by the given amount

    :param image: The image to be changed (Numpy array)
    :param change: the change (integer) (The min brightness is 0 and max is 100)

    :param hsv_image: bool noting if the image is in hsv
    :return: a copy of the image changed
    """
    image = image if hsv_image else cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    change = change * 2.55
    vid = image[:, :, 2]
    if change > 0:
        vid = np.where(vid + change <= 255, vid + change, 255)
    else:
        vid = np.where(vid + change >= 0, vid + change, 0)
    image[:, :, 2] = vid
    image = image if hsv_image else cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image


def _rotate_shortcut(image, shortcut_angle):
    """
    Return a copy of the image rotated 90 degrees to the left (_counter-clockwise)

    :param image: numpy array, image to be rotated
    :return: a copy of the image rotated.
    """
    (height, width) = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, shortcut_angle, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (height, width))


SHORTCUT_ANGLES = {
    90: _rotate_shortcut,
    180: _rotate_shortcut,
}


@image_filter
def rotate_image(image: np.ndarray, angle: int = 180) -> np.ndarray:
    """
    Rotates an image by a given amount of degrees.
    Note that the rotated image's dimensions will most likely change if
    the angle is not 90, -90, 180, 0 or a multiplication of them)

    :param image: the image to be rotated
    :param angle: the angle to rotate the image in degrees (positive is to the left, negative to the right)
    :return: the rotated image
    """
    angle = abs(angle % 360)
    if angle in SHORTCUT_ANGLES:
        return SHORTCUT_ANGLES[abs(angle)](image, angle)
    elif angle == 0:
        return image
    else:
        return _rotate_by_angle(image, angle)


def _rotate_by_angle(image, angle):
    """
    Rotates the given image by a given angle
    The new image will have different dimensions if the rotation angle isn't a multiple of 90

    This is an inner function that is not an image_filter.
    Use rotate_by_angle (no underscore) to rotate an image, using shortcuts for certain angles


    :param image: the image to be rotated
    :param angle: the angle of rotation
    :return: the rotated image
    """
    (height, width) = image.shape[:2]
    center_xy = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center_xy, -angle, 1.0)
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    rotated_image_dimensions = (int((height * sin) + (width * cos)), int((height * cos) + (width * sin)))
    rotation_matrix[0, 2] += (rotated_image_dimensions[0] / 2) - center_xy[0]
    rotation_matrix[1, 2] += (rotated_image_dimensions[1] / 2) - center_xy[1]
    return cv2.warpAffine(image, rotation_matrix, rotated_image_dimensions)


@image_filter
def non_local_mean_denoising(image, h=10, hColor=None, template_window_size=None, search_window_size=None,
                             destination=None):
    """
    Non local mean denoising is an image noise removal function.
    Non local mean denoising removes noise by finding matching patterns in other parts of the image
    It has different arguments for greyscale images and color images

    :param image: the image to be denoised
    :param hColor:
    :param h: parameter deciding filter strength. Higher h value removes noise better,
     but removes details of image also. (10 is default)
     h maps to h in the greyscale version of the opencv function and to hColor in the color version
    :param template_window_size: size of the template window, should be an odd number
    :param search_window_size: size of the search window
    :param destination: an image of the same size to place the result
    :return: the denoised image, a numpy array

    For more information about the implementation please refer the the opencv source code
    and this tutorial:
    https://docs.opencv.org/3.4/d5/d69/tutorial_py_non_local_means.html

    For more information on the algorithim behind the implementation look at this
    paper:
    http://www.ipol.im/pub/art/2011/bcm_nlm/
    """
    parameters = {"h": h,
                  "hColor": hColor,
                  "templateWindowSize": template_window_size,
                  "seasonWindowSize": search_window_size,
                  "dst": destination
                  }
    return cv2.fastNlMeansDenoisingColored(image,
                                           **remove_none_values(parameters))


@image_filter
def gaussian_blur(image, kernel_size=DEFAULT_KERNEL_SIZE, sigma_x=5, sigma_y=None, border_type=None):
    """
    An image filter version of cv2.gaussianBlur.

    Gaussian blur is a common filter that is used to remove image noise.

    It is considered necessary when preforming edge detection (such as using the CannyThreshold)

    Gaussian Blur assumes the noise in the image is random and that the neighbors of each pixel
    are similar in a normally distributed fashion, meaning the closer the neighbor the more it should
    be similar to the pixel. The process of applying the kernel to the image is called convolution.

    :param image: the image to be blurred (numpy array)
    :param kernel_size: the size of the window that moves over the image
    this determines what are the pixel's neighbors. The kernel must be of odd dimensions
    so that it has a center pixel - which is where the output is placed
    :param sigma_x: standard distribution of the gaussian function on the x axis,
    the larger this is the more further neighbors affect the new value of the window's center
    :param sigma_y: standard distribution of the gaussian function on the y axis,
    the larger this is the more further neighbors affect the new value of the window's center
    if this is set to 0 or None then it will take the value of sigma_x
    :param border_type: Specifies image boundaries while kernel is applied on image borders.

    More information on these can be found in the opencv's gaussianBlur function
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html#gaussian-filtering
    :return: the blurred image
    """
    parameters = {"ksize": kernel_size,
                  "sigmaX": sigma_x,
                  "sigmaY": sigma_y,
                  "borderType": border_type}
    return cv2.GaussianBlur(image, **remove_none_values(parameters))


@image_filter
def crop_image(image, point: Tuple[int, int], dimensions: Tuple[int, int]):
    """
    Crops a given rectangle from a given image, this can be used to "cut out"
    a rectangle part of the image.

    The rectangle is defined by the origin (point) a tuple of (x, y) denoting the top left corner
    and by the dimensions of its sides - defined using a tuple of (width, height).

    :param image: an image (numpy array)
    :param point: (x, y) coordinates that is the top left corner of the rectangle
    :param dimensions: (width, height) of the rectangle
    :return: the region of the image
    """
    x, y = point
    width, height = dimensions
    return image[x: x + width, y: y + height]


@image_filter
def undistort(image, camera_matrix, distortion_coefficients, destination=None, new_camera_matrix=None):
    """
    Using calculated camera matrix and distortion coefficients can be used to remove distortions caused
    by the camera and manufacturing flaws. Getting the camera matrix and distortion coefficients requires
    performing camera calibration (usually using a chessboard)
    For more information on camera calibration:
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html


    :param image: the ndarray of the image
    :param camera_matrix: the camera matrix that was calculated from the camera calibration
    :param distortion_coefficients: the distortion coefficients that were calculated from the camera calibration
    :param destination: the image the result should be saved in, None if just return
    :param new_camera_matrix: the new optimal camera matrix .
    :return: the undistorted image
    """
    parameters = {
        "destination": destination,
        "new_camera_matrix": new_camera_matrix
    }
    return cv2.undistort(image, camera_matrix, distortion_coefficients, **remove_none_values(parameters))
