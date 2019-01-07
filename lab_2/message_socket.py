from socket import socket

class MessageSocket:

    def __init__(self, client_socket: socket):
        self.socket: socket = client_socket
        self.buffer = bytes(0)
        self.closed = False

    def recv_message(self):
        try:
            message_length = int(self._read_bytes(1))
        except ValueError:
            self.close()
            return None

        return self._read_bytes(message_length)

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
            self.buffer += self.socket.recv(4096)
