from typing import Union, Tuple, Any

import numpy as np

VisionLike = Union["Vision", "AmbientVision"]


Target = Union[np.ndarray, Tuple, Any]


def RangedNumber(start, end):
    class Hint:
        def __class_getitem__(cls, item):
            cls.start = item[0]
            cls.end = item[1]
            return cls
    return Union[float, Hint[start, end]]


