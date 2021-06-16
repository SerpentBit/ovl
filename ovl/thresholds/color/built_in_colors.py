from enum import Enum

from .color import Color
from .multi_color import MultiColor


class HSVColors(Enum):
    """
    There are multiple built in "battery included" pre-made color object
        for instant use in testing and tuning
        List of colors:
          Red (MultiColorObject) : Red (low) + Red (high)
          Red (Low): [0, 100, 100], [8, 255, 255]
          Red (High): [172, 100, 100], [179, 255, 255]
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
    yellow_hsv = Color([20, 100, 100], [55, 255, 255])
    blue_hsv = Color([100, 100, 100], [135, 255, 255])
    green_hsv = Color([35, 100, 100], [75, 255, 255])
    purple_hsv = Color([130, 100, 100], [170, 255, 255])
    orange_hsv = Color([10, 100, 100], [18, 255, 255])
    red_low_hsv = Color([0, 100, 100], [15, 255, 255])
    red_high_hsv = Color([170, 100, 100], [179, 255, 255])
    red_hsv = MultiColor([red_high_hsv, red_low_hsv])
    white_hsv = Color([0, 0, 200], [179, 20, 255])
    black_hsv = Color([110, 0, 0], [130, 255, 30])
    grey_hsv = Color([0, 0, 0], [179, 50, 195])
    teal_hsv = Color([80, 50, 60], [95, 255, 155])











