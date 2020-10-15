import numpy as np


class CameraSettings:
    def __init__(self, camera_offset, camera_calibration):
        self.camera_offset = camera_offset
        self.camera_calibration = camera_calibration
        self.image_dimensions = None

    def undistort_image(self, image: np.ndarray) -> np.ndarray:
        """
         Removes distortion created by imperfections in the camera.
        :param image: The image (numpy ndarray) that should be undistorted.
        :return: an undistorted copy of the image
        """
        return self.camera_calibration.undistort_image(image)
