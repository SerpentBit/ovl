# Copyright 2018 - 2019 Ori Ben-Moshe - All rights reserved.
from threading import Thread
import cv2


class Camera:
    """
    A camera object used to take images in a higher fps than cv2.VideoCapture
    """
    def __init__(self, src=0, width=320, height=240):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, width)
        self.stream.set(4, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        """
        Action: Returns the ret val and the frame
        :return: return val (if image taking was successful), the image numpy
        :rtype: bool, numpy.array
        """
        return self.grabbed, self.frame

    def stop(self):
        """
        Stops the camera thread.
        :return:
        """
        self.stopped = True

    def release(self):
        """
        Action: stops the camera thread and releases the camera
        :return: None
        """
        self.stopped = True
        self.stream.release()

    def set(self, prop_id, value):
        """
        Action: sets the value of the given property to the given value
         :param prop_id: the proprety number, for more information:
                        https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html
        :param value: the value to be set, a number
        :return: None
        """
        self.stream.set(prop_id, value)

    def get(self, prop_id):
        """
        Action: retrieves the value of a property based on its id
        :param prop_id: the proprety number, for more information:
                        https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html
        :return: the value
        """
        return self.stream.get(prop_id)

    def isOpened(self):
        """
        Returns true if the camera is opened and false otherwise
        :return:
        :rtype: bool
        """
        return self.isOpened()

    def getBackendName(self):
        """
        Action: returns the Back end name of a camera
        :return:
        """
        return self.stream.getBackendName()
