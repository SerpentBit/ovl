from typing import NewType, Callable, Union

import math

TargetSelector = NewType("TargetSelector", Union[Callable, int, tuple])


def validate_target_selector(target_selector: TargetSelector):
    if not isinstance(target_selector, (Callable, int, tuple)):
        raise TypeError("Target selector must be an int, a tuple of 2 ints or a function that receives the targets,"
                        f"target_selector: {target_selector}")
    if isinstance(target_selector, int):
        return target_selector if target_selector <= 0 else math.inf
    if isinstance(target_selector, tuple):
        try:
            low, high = target_selector
            if not (0 <= low < high):
                raise ArithmeticError("If target selector is a tuple, low must be bigger or equal to 0,"
                                      f" and high must be bigger that low, target_selector:  {target_selector}")
            return target_selector
        except (TypeError, ValueError):
            raise TypeError(f"If target selector is a tuple it must be of length 2! target_selector: {target_selector}")
    if isinstance(target_selector, Callable):
        return target_selector
    return target_selector
