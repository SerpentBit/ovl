from .color import Color
from .multi_color import MultiColor

# TODO: ADD default retro-reflective tape color with green leds
"""
There are multiple built in "battery included" pre-made color object
    for instant use in testing and tuning
    List of colors:
      Red (MultiColorObject) : Red (low) + Red (high)
      Red (Low): [0, 100, 100], [8, 255, 255]
      Red (High): [172, 100, 100], [179, 255, 255]
      Note: in order to find red, use both ranges (low and high) and use the some of both results.
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

YELLOW_HSV = Color([20, 100, 100], [55, 255, 255])
BLUE_HSV = Color([100, 100, 100], [135, 255, 255])
GREEN_HSV = Color([35, 100, 100], [75, 255, 255])
PURPLE_HSV = Color([130, 100, 100], [170, 255, 255])
ORANGE_HSV = Color([10, 100, 100], [18, 255, 255])
RED_LOW_HSV = Color([0, 100, 100], [15, 255, 255])
RED_HIGH_HSV = Color([170, 100, 100], [179, 255, 255])
RED_HSV = MultiColor([RED_HIGH_HSV, RED_LOW_HSV])
WHITE_HSV = Color([0, 0, 200], [179, 20, 255])
BLACK_HSV = Color([110, 0, 0], [130, 255, 30])
GREY_HSV = Color([0, 0, 0], [179, 50, 195])
TEAL_HSV = Color([80, 50, 60], [95, 255, 155])

COLORS = {"YELLOW_HSV": YELLOW_HSV,
          "BLUE_HSV": BLUE_HSV,
          "ORANGE_HSV": ORANGE_HSV,
          "PURPLE_HSV": PURPLE_HSV,
          "RED_HSV": RED_HSV,
          "GREEN_HSV": GREEN_HSV,
          "GREY_HSV": GREY_HSV,
          "WHITE_HSV": WHITE_HSV,
          "BLACK_HSV": BLACK_HSV,
          "TEAL_HSV": TEAL_HSV}
