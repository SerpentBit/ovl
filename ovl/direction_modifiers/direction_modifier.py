from typing import Union


class DirectionModifier:
    @property
    def priority(self) -> Union[bool, float]:
        """
        This is a value that determines the Modifier's priority.
        Determines whether it skips following DirectionModifiers.

        """
        return False

    def modify_directions(self, directions, targets, image):
        """
        Use this function to define behaviour that is applied to the directions you calculate.
        This can range from:
            - deciding when to stop
            - correcting camera location in comparison to the robot turn axis (i.e. Indentation)
            - applying some sort of pid on directions
            - convert the values to different scale or unit
            - saving data for analysis
            - interpolation the data from the directions calculated
            - anything else you wish to apply as a "logical" change on object detection behaviour
        :param image: the image the pipeline ran on.
        :param targets: the list of targets found at the end of the filtration
        :param directions: the result of the direction function
        :return: the modified direction
        """
        raise NotImplementedError("When inheriting DirectionMonitor you must implement it!")
