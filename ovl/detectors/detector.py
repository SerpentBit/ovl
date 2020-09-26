from typing import List, Any


class Detector:
    """
    Detector the class that implements the Detection stage of the pipeline

    The only required function is detect which should get an image and return

    """
    def detect(self, image, *args, **kwargs) -> List[Any]:
        raise NotImplemented()
