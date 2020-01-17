from abc import abstractmethod


class Threshold:
    @abstractmethod
    def convert(self, image):
        pass

    @abstractmethod
    def validate(self, *args, **kwargs) -> bool:
        pass
