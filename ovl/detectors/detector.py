from abc import ABC, abstractmethod
from typing import List, Any

from ..api.object_apis import Serializable


class Detector(ABC, Serializable):
    """
    Detector the class that implements the Detection stage of the pipeline

    The only required function is detect which should get an image and return

    """
    @abstractmethod
    def detect(self, image, *args, **kwargs) -> List[Any]:
        raise NotImplemented()

    @abstractmethod
    def __repr__(self):
        raise NotImplemented()
