from socket import socket


class UnexpectedConnectionClose(Exception):
    pass


class MessageSocket:

    def __init__(self, client_socket: socket):
        self.socket: socket = client_socket
        self.closed: bool = False

    def recv_message(self) -> bytes:
        raise NotImplementedError

    def send_message(self, message: bytes):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class PrefixedMessageSocket(MessageSocket):

    def __init__(self, client_socket: socket):
        super().__init__(client_socket)
        self.buffer = bytes(0)

    def recv_message(self):
        if self.closed:
            return None

        try:
            message_length = int(self._read_bytes(1))
        except ValueError:
            self.close()
            return None

        return self._read_bytes(message_length)

    def send_message(self, message: bytes):
        if self.closed:
            return

        self.socket.send(message)

    def close(self):
        self.socket.close()
        self.closed = True

    def _read_bytes(self, size):
        self._ensure_buffer_size(size)

        _bytes = self.buffer[:size]
        self.buffer = self.buffer[size:]
        return _bytes

    def _ensure_buffer_size(self, size):
        while len(self.buffer) < size:
            new_bytes = self.socket.recv(4096)
            if len(new_bytes) == 0:
                self.closed = True
                raise UnexpectedConnectionClose
            self.buffer += new_bytes


class DelimitedMessageSocket(MessageSocket):

    def __init__(self, client_socket: socket, delimiter="\r\n"):
        super().__init__(client_socket)
        self.buffer = bytes(0)
        self.delimiter = bytes(delimiter, encoding="ascii")

    def recv_message(self):
        if self.closed:
            return None

        while self.delimiter not in self.buffer:
            self._receive_more_bytes()

        message, leftover = self.buffer.split(self.delimiter, 1)
        self.buffer = leftover

        return message

    def send_message(self, message: bytes):
        if self.closed:
            return

        self.socket.send(message + self.delimiter)

    def close(self):
        self.socket.close()
        self.closed = True

    def _receive_more_bytes(self):
        new_bytes = self.socket.recv(4096)
        if len(new_bytes) == 0:
            raise UnexpectedConnectionClose
        self.buffer += new_bytes

