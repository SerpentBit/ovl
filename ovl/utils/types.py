from typing import Union, Tuple, Any

import numpy as np

VisionLike = Union["Vision", "AmbientVision"]


Target = Union[np.ndarray, Tuple, Any]


def RangedNumber(start, end):
    class Hint:
        def __class_getitem__(self, item):
            self.start = item[0]
            self.end = item[1]
            return self
    return Union[float, Hint[start, end]]


