import cv2
import numpy as np

from .detector import Detector


class HaarCascadeDetector(Detector):
    """
    A detector used to detect objects using haar cascade algorithm
    The Detector initializes using a xml file containing the descriptor

    The Detector uses the underlying cv2.CascadeClassifier

    For more information on

    """
    def __init__(self, classifier: str):
        self.classifier_source = classifier
        self.classifier = cv2.CascadeClassifier(classifier)

    def detect(self, image: np.ndarray, *args, **kwargs):
        greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.classifier.detectMultiScale(greyscale)
