from abc import abstractmethod

from api.object_apis import Serializable


class Threshold(Serializable):
    """
    Threshold is a base class for Threshold object that threshold an image
    (Color, binary or otherwise), threshold is then followed up
    """

    @abstractmethod
    def threshold(self, image):
        pass

    @abstractmethod
    def validate(self, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def __repr__(self):
        pass
