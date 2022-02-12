from enum import Enum
from typing import Any

from .connection import Connection


class HTTPRequestTypes(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"


class HTTPConnection(Connection):
    """
    A Connection that utilizes HTTP

    HTTP is useful for communicating with HTTP Servers over the web, although slower than other more
    low level connection types
    """

    def __init__(self, session, default_url=None, headers=None, auth=None):
        import requests
        self.session = session or requests.Session()
        self.session.headers.update(headers)
        if auth:
            self.auth = auth
            self.session.auth(auth)
        self.url = default_url

    def __enter__(self):
        return self.session.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.session.__exit__(exc_type, exc_val, exc_tb)

    def send_request(self, data: Any, url: str, method: HTTPRequestTypes, raise_for_status=True, **kwargs):
        """
        send_request is the function used to send a request using HTTP protocol.
        This can be used to send request to servers running remotely in the internet or to an HTTP server in the LAN.


        Note: This is the inner function used by the Connection object to send and receive.
        The functions send, receive and interval_receive should be used instead!


        :param data: The data to be passed as the request's payload
        :param url: the url to send the request to
        :param method: the HTTP method to be used
        :param kwargs: any other parameters to `requests.request`
        :param raise_for_status: raise an exception if the request failed, uses `request.raise_for_status()`
        :return: the response received for the request
        """
        import requests
        params = {"data": data}
        if "params" in kwargs.keys():
            params = {**kwargs["params"], "data": data}
        url = url or self.url
        response = requests.request(method.value, url, params=params, **kwargs)

        if raise_for_status:
            response.raise_for_status()
        return response

    def send(self, data: Any, url: str = None, method=HTTPRequestTypes.POST, **kwargs):
        """
        Sends an HTTP requests, should be used to only send data and not receive any data
        as it represent the logical action of sending information

        :param data: the data to be sent, passed
        :param url: the url to send it to
        :param method: the request method (GET, POST, DELETE etc.)
        :param kwargs: any other parameter to be passed the request ()
        :return:
        """
        return self.send_request(data, url, method, **kwargs)

    def receive(self, data: Any = None, url: str = None, method: HTTPRequestTypes = HTTPRequestTypes.GET, **kwargs):
        """
        Receive for HTTPConnection is a bit different compared to other Connection in that it sends a request
        and returns a response which is the main usage, in addition the interval parameter allows for high
        interval sampling (for MultiVision for example) without sending many requests

        :param url: the url to send to, overrides self.url
        :param data: any data to pass with the requests
        :param method: determines what HTTP method should the request use (GET, POST, PUT etc.)
        :param kwargs: any other parameters passed to `requests.request`
        :return:
        """
        return self.send_request(data, url, method, **kwargs)
