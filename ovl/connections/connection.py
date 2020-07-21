from .network_location import NetworkLocation


class Connection:
    def send(self, data, *args, **kwargs):
        """
        Used to send information to an external source,
        send represents outgoing information, usually over-network but not exclusively

        :param data: the data to be sent, a common use is sending the directions from direction objects after
        object detection
        :param args: any additional arguments for the specific connection object
        :param kwargs: any additional keyword arguments for the specific connection object
        :return:
        """
        pass

    def receive(self, *args, **kwargs):
        """
        Used to receive information from an external source,
        receive represents incoming information, usually over-network but not exclusively
        Receive can be used to send a request in order to receive
        for example HttpConnection send an http request and returns the response data

        :param args: any additional arguments for the specific connection object
        :param kwargs: any additional keyword arguments for the specific connection object
        :return:
        """
        pass

    def receive_from_location(self, network_location: NetworkLocation, *args, **kwargs):
        """
        Used to receive information from an external source,
        receive represents incoming information, usually over-network but not exclusively

        Receive can be used to send a request in order to receive
        for example HttpConnection send an http request and returns the response data

        Receive_from_location uses a NetworkLocation to specify

        :param network_location: used to specify parameters of a specific "location"
        or information about the receipt.
        :param args: any additional arguments for the specific connection object
        :param kwargs: any additional keyword arguments for the specific connection object
        :return:
        """
        return self.receive(*args, **network_location, **kwargs,)

    def send_to_location(self, data, network_location: NetworkLocation, *args, **kwargs):
        return self.receive(*args, **network_location, **kwargs, data=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        pass
