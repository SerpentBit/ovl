from abc import abstractmethod


class Threshold:
    """
    Threshold is a base class for Threshold object that threshold an image
    (Color, binary or otherwise), threshold is then followed up
    """
    @abstractmethod
    def convert(self, image):
        pass

    @abstractmethod
    def validate(self, *args, **kwargs) -> bool:
        pass
