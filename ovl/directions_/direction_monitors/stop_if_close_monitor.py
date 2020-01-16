import typing
import numpy as np

from ...math_ import geometry
from ..direction_monitors.direction_monitor import DirectionMonitor


class StopIfCloseMonitor(DirectionMonitor):
    """
    A Direction monitor that stops when the target found is large enough (close enough).
    Like other DirectionMonitor objects, it monitors the directions returned.
    """
    def __init__(self, minimum_size: float, value_sent: typing.Any, priority: bool = False):
        """
        :param minimum_size: This is the size in pixels that considers the object "close" enough
                            it depends on your object size, but 40% of the image size is usually enough
                            so for an image the size of 320 x 240 it will be 320 * 240 * 0.4
        :param value_sent: the value returned if the object is close enough
        :param priority: a boolean that notes if this monitor should take priority (and stop following monitors from
                         being called)
        WARNING: Setting priority to true can cause 'unexpected' behaviour as a result of stopping
        """
        self.minimum_size = minimum_size
        self.value_sent = value_sent
        self._priority = priority

    @property
    def priority(self):
        return self._priority

    def monitor(self, directions: typing.Any, target_contours: typing.List[np.ndarray],
                image: np.ndarray, mask: np.ndarray) -> typing.Any:
        if geometry.target_size(target_contours) >= self.minimum_size:
            return self.value_sent
        return directions
