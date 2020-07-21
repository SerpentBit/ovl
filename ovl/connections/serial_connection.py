import typing

from .connection import Connection


class SerialConnection(Connection):
    """
    Serial connection is a Connection used to send and receive on a Serial bus like various USB cables.

    SerialConnection is implemented under the hood using Pyserial and it is a package requirement for
    using SerialConnection, make sure it is installed by executing in console:

    pip install pyserial

    """
    def __init__(self, port: typing.Union[int, str], baudrate: int = 9600, *args, **kwargs):
        from serial import Serial

        self.socket = Serial(port, baudrate, *args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def send(self, data, *args, **kwargs):
        self.socket.write(data)

    def receive(self, *args, **kwargs):
        return self.socket.read(*args, **kwargs)
