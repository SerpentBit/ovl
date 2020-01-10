import typing

from .connection import Connection


class SerialConnection(Connection):
    def __init__(self, port: typing.Union[int, str], baudrate: int = 9600, *args, **kwargs):
        from serial import Serial

        self.socket = Serial(port, baudrate, *args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def send(self, data, *args, **kwargs):
        self.socket.write(data)

    def receive(self, *args, **kwargs):
        return self.socket.read()
