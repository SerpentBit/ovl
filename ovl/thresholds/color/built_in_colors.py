import enum

from .color import Color
from .multi_color import MultiColor
from ..threshold import Threshold

"""
There are multiple built in "battery included" pre-made colors objects
for instant use in testing and tuning
"""
RED_LOW_HSV = Color([0, 100, 100], [15, 255, 255])
RED_HIGH_HSV = Color([170, 100, 100], [179, 255, 255])


class HSV(Threshold, enum.Enum):
    """
      List of colors:
      Red (MultiColorObject) : [0, 100, 100], [8, 255, 255] and [172, 100, 100], [179, 255, 255]
      Blue: [105, 100, 100], [135, 255, 255]
      Green: [45, 100, 100], [75, 255, 255]
      Yellow: [20, 100, 100], [55, 255, 255]
      Orange: [10, 100, 100], [18, 255, 255]
      Grey: [0, 0, 0], [179, 50, 195]
      Black: [0, 0, 0], [179, 255, 30]
      White: [0, 0, 200], [179, 20, 255]
      Teal: [110, 100, 100], [130, 255, 255]
      Purple: [135, 100, 100], [165, 255, 255]
    """

    def __repr__(self):
        return f"HSV.{self.name}({self.value})"

    def serialize(self):
        pass

    @classmethod
    def deserialize(cls, data):
        pass

    def threshold(self, image):
        return self.value.threshold(image)

    def validate(self, *args, **kwargs) -> bool:
        return self.value.validate(*args, **kwargs)

    red = MultiColor([RED_HIGH_HSV, RED_LOW_HSV])
    orange = Color([9, 50, 50], [21, 255, 255])
    yellow = Color([24, 50, 50], [34, 255, 255])
    green = Color([35, 50, 50], [75, 255, 255])
    blue = Color([90, 50, 50], [123, 255, 255])
    purple = Color([125, 50, 50], [145, 255, 255])
    white = Color([0, 0, 200], [179, 20, 255])
    black = Color([110, 0, 0], [130, 255, 30])
    grey = Color([0, 0, 0], [179, 50, 195])
    teal = Color([80, 50, 60], [95, 255, 155])

