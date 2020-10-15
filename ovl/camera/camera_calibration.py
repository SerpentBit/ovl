import cv2


class CameraCalibration:
    def __init__(self, object_points, image_points, image_dimensions, alpha=0, save_raw=False):
        self.image_dimensions = image_dimensions
        if save_raw:
            self.image_points = image_points
            self.object_points = object_points
        else:
            self.image_points = None
            self.object_points = None
        calibration = cv2.calibrateCamera(object_points, image_points, image_dimensions, None, None)
        (_, camera_matrix, distortion_coefficients,
         rotation_vectors, translation_vectors) = calibration
        optimal_matrix, region_of_image = cv2.getOptimalNewCameraMatrix(camera_matrix,
                                                                        distortion_coefficients,
                                                                        image_dimensions,
                                                                        alpha)
        self.optimal_matrix = optimal_matrix
        self.region_of_image = region_of_image
        self.camera_matrix = camera_matrix
        self.rotation_vectors = rotation_vectors
        self.translation_vectors = translation_vectors
        self.distortion_coefficients = distortion_coefficients

    def undistort_image(self, image):
        """
         Removes distortion created by imperfections in the camera.
        :param image: The image (numpy array) that should be undistorted
        :return: an undistorted copy of the image
        """
        return cv2.undistort(image, self.camera_matrix, self.distortion_coefficients, None, self.optimal_matrix)
