import typing

VisionLike = typing.Union["Vision", "AmbientVision"]


def RangedNumber(start, end):
    class Hint:
        def __class_getitem__(cls, item):
            cls.start = item[0]
            cls.end = item[1]
            return cls
    return typing.Union[float, Hint[start, end]]
