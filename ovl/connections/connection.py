from .network_location import NetworkLocation


class Connection:
    def send(self, data, *args, **kwargs):
        pass

    def receive(self, *args, **kwargs):
        pass

    def receive_from_location(self, network_location: NetworkLocation, *args, **kwargs):
        return self.receive(*args, **network_location, **kwargs,)

    def send_to_location(self, data, network_location: NetworkLocation, *args, **kwargs):
        return self.receive(*args, **network_location, **kwargs, data=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        pass
