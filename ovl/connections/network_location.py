from typing import Any


class NetworkLocation:
    """
    An object used to specify parameters for a Connection.send  and Connection.receive functions
    This is used to create a specific address / port for a connection and allows automated specification
    for a place to send / receive.

    A common use is for MultiVision to specify a "location" from which to read the current vision to be used.
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def keys(self):
        return self.kwargs.keys()

    def __getitem__(self, key) -> Any:
        return self.kwargs[key]
