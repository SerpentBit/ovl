import functools
import sys

from cloudpickle.cloudpickle import _PICKLE_BY_VALUE_MODULES
import cloudpickle

from ..partials.reverse_partial import ReversePartial


def serialize_target_filter(target_filter):
    if isinstance(target_filter, functools.partial):

    module = target_filter.__module__
    if module not in sys.modules:
        raise ValueError(
            f"{module} was not imported correctly, have you used an "
            f"`import` statement to access it?"
        )
    _PICKLE_BY_VALUE_MODULES.add(module)
    return cloudpickle.dumps(target_filter)

