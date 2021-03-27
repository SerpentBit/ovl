from typing import Union


class DirectionModifier:
    @property
    def priority(self) -> Union[bool, float]:
        """
        This is a value that determines whether or not it stop consecutive DirectionModifiers

        :return:
        """
        return False

    def monitor(self, directions, targets, image):
        """
        This is the function
        :param directions:
        :param targets:
        :param image:
        :return:
        """
        raise NotImplementedError("When inheriting DirectionMonitor you must implement it!")
