from typing import Any, Union

from .connection import Connection
from ..helpers.team_number_to_ip import team_number_to_ip

NetworkTables = None


class NetworkTablesConnection(Connection):
    """
    Note: In Order to use NetworkTablesConnection you must have pynetworktables installed. (It is automatically installed
    when installing ovl)

    A connection to that uses NetworkTables (The FRC network protocol).

    NetworkTables are a group of Dictionaries (Hash tables) that are shared by all computers in the network.
    In the case of the FRC it is created by the RoboRIO and shared by other
    computers on the network like: the driver station, any connected co-processor (like a raspberry pi) etc.

    NetworkTablesConnection creates defaults to writing to the Vision table.
    You can then read from /vision/vision_result the result sent.

    For Additional information about NetworkTables
    please refer to:
    https://docs.wpilib.org/en/latest/docs/software/networktables/networktables-intro.html
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
        self.table_cache = {table_name: self.table}
        self.table_name = table_name

    def get_table(self, table):
        """
        Fetches a table by name, if table exists in cache it returns
        the cached table instead.
        If table is none it returns the default table (set in the constructor)

        :param table: the name of the table examples: "usage", "SmartDashboard", "vision"
        if it doesnt exist it is created
        :return: the table
        """
        from networktables import NetworkTables
        if table is None:
            table = self.table
        elif table in self.table:
            table = self.table_cache[table]
        else:
            table_name = table
            table = NetworkTables.getTable(table)
            self.table_cache[table_name] = table
        return table

    def send(self, data, table_key: Union[str, Any] = None,
             table: Union[str, Any] = None, *args, **kwargs) -> None:
        """
        A function used to put a value in a given table and key in the connected
        NetworkTable.
        For more information about NetworkTables functionality
        please refer to:
        https://docs.wpilib.org/en/latest/docs/software/networktables/networktables-intro.html

        :param data: the data to send (post to the NetworkTables)
        :param table_key: the specific table to read from
        :param table: the table to receive from. Examples are SmartDashboard
                      or Usage. Use "Vision" if you are not sure)
        """
        table_key = table_key if table_key else self.table_key
        table = self.get_table(table)
        return table.putValue(table_key, data)

    def receive(self, table_key: str = None, table: str = None, default_value=None, *args, **kwargs) -> Any:
        """
        Gets a value from a specific key and table, can be used to read values shared by
        all computers in the network.

        Default table and table keys are the ones initialized.

        .. code-block:: python

            import ovl

            TEAM_NUMBER = "1937"
            connection = ovl.NetworkTablesConnection(TEAM_NUMBER)

            connection.send("hello", table_key="my_key")

            print(connection.receive(table_key="my_key"))
            # prints "hello"


        :param table_key: the specific table to read from, None
        :param table: the table to receive from (Use "Vision" if you are not sure)
        :param default_value: the value to return if the given table key does not exist
        """
        table = self.get_table(table)
        table_key = table_key or self.table_key
        return table.getValue(table_key, default_value)
