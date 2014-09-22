import json
import select
import socket
import time


class OVSDBClient(object):

    # ===========
    # EXCEPTIONS
    # ===========

    class ConnectionError(Exception):

        def __init__(self, hostname, port, errno, message):
            message = "Unable to connect to %s:%s. More info: (%i) %s" \
                % (hostname, port, errno, message)

            super(self.__class__, self).__init__(message)

    class ReceiveTimeoutError(Exception):

        def __init__(self, timeout, buff):
            if not buff:
                buff = "<EMPTY>"
            message = "Did not get a notification after %i seconds. " \
                      "Data received so far: %s" % (timeout, buff)

            super(self.__class__, self).__init__(message)

    class RequestTimeoutError(Exception):

        def __init__(self, formatted_json, timeout, buff):
            if not buff:
                buff = "<EMPTY>"
            message = "Request timed out after %i seconds. Request " \
                      "details: %s. Data received so far: %s" \
                      % (timeout, formatted_json, buff)

            super(self.__class__, self).__init__(message)

    # ===========
    # INITIALIZER
    # ===========

    def __init__(self, hostname=None, port=None, request_timeout=5):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._socket.connect((hostname, port))
        except socket.error as (errno, message):
            raise OVSDBClient.ConnectionError(hostname, port, errno, message)

        self._request_timeout = request_timeout

    # =================
    # PUBLIC PROPERTIES
    # =================

    @property
    def buffer(self, max_chunk_size=12288):
        try:
            ready_to_read, ready_to_write, in_error = \
                select.select([self._socket], [], [], 0)
            if self._socket in ready_to_read:
                self._buffer += self._socket.recv(max_chunk_size)
            else:
                self._buffer += ""
        except socket.error:
            self._buffer += ""

        return self._buffer

    # ===============
    # PUBLIC METHODS
    # ===============

    def receive(self):
        self._flush_buffer()
        message = ""
        start = time.time()

        while len(message) == 0 or message.count("}") < message.count("{"):
            message = self.buffer
            duration = time.time() - start
            if duration > self._request_timeout:
                raise OVSDBClient.ReceiveTimeoutError(duration, message)

        return json.loads(message)

    def request(self, dict):
        message = json.dumps(dict)
        self._flush_buffer()

        self._socket.send(message)

        response = ""
        start = time.time()

        while len(response) == 0 or \
                response.count("}") < response.count("{"):
            response = self.buffer
            duration = time.time() - start
            if duration > self._request_timeout:
                raise OVSDBClient.RequestTimeoutError(
                    message, duration, response)

        return json.loads(response)

    def send(self, dict):
        self._flush_buffer()
        self._socket.send(json.dumps(dict))

    # ================
    # PRIVATE METHODS
    # ================

    def _flush_buffer(self):
        self._buffer = ""
