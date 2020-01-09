from typing import Any, Union

from .connection import Connection
from ..helpers_.team_number_to_ip import team_number_to_ip


class NetworkTablesConnection(Connection):
    """
    Note: In Order to use NetworkTablesConnection you must have pynetworktables installed.

    A connection to Networktables (The FRC network protocol)
    NetworkTables are a group of Dictionaries (Hash tables) that are shared by all computers in the network.
    NetworkTablesConnection creates defaults to writing to the Vision table.
    You can then read from /vision/vision_result the result sent.
    """

    def __init__(self, roborio: str, table_name: str = "Vision", table_key: str = "vision_result"):
        """
        :param roborio: team number, roborio hostname or ip.
            for a team number 1234 valid inputs are:
              - 1234
              - roboRIO-1234-FRC.local
              - 10.12.34.2 (10.TE.AM.2)
              - a dynamic ip of the roborio
        NOTE: When using static ip (relevant inputs: 1234 and 10.12.34.2)
              make sure both your computer and the roborio are set to have a static ip
              for more information:
              https://docs.wpilib.org/en/latest/docs/networking/networking-introduction/index.html
        :param table_name: the table to use as a default "Vision" is recommended
        :param table_key: the key in the table to use as a default
        """
        from networktables import NetworkTables
        if roborio.isnumeric():
            roborio = team_number_to_ip(roborio)
        self.roborio_ip = roborio
        self.connection = NetworkTables.initialize(roborio)
        self.table_key = table_key
        self.table = NetworkTables.getTable(table_name)
        self.table_name = table_name

    def send(self, data, table_key: Union[str, None] = None,
             table: Union[str, None] = None, *args, **kwargs) -> None:
        """
        :param data: the data to send (post)
        :param table_key: the specific table to read from
        :param table: the table to receive from (Use "Vision" if you are not sure)
        """

        table_key = table_key if table_key else self.table_key
        return self.table.putValue(table_key, data)

    def receive(self, table_key: str = None, table: str = None,
                default_value=None, *args, **kwargs) -> Any:
        """
        Gets a value from network tables from which to read a value
        :param table_key: the specific table to read from
        :param table: the table to receive from (Use "Vision" if you are not sure)
        :param default_value: the value to return if the given table key does not exist
        """
        table = table or self.table
        table_key = table_key or self.table_key
        return table.getValue(table_key, default_value)
