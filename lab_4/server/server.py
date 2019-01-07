import logging
from socket import socket
from threading import Thread

from .database import Storage, SQLiteStorage
from .message_socket import MessageSocket, DelimitedMessageSocket, \
    UnexpectedConnectionClose


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket()
        self.storage: Storage = SQLiteStorage()

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        logger.info(f"Server started on port {self.port}")

        while True:
            client_socket, address = self.socket.accept()
            logger.info(f"New connection from {address}")
            client = DelimitedMessageSocket(client_socket)

            client_thread = Thread(
                target=self.handle_connection,
                args=(client, address))
            client_thread.start()

    def handle_connection(self, client: MessageSocket, address):
        while not client.closed:
            try:
                message: bytes = client.recv_message()
            except UnexpectedConnectionClose:
                logger.info(f"Connection to {address} closed abruptly")
                return

            logger.debug(f"Received message from {address}: {message}")

            if message is None:
                break
            if len(message) == 0:
                client.close()
                break
            elif message.startswith(b's'):
                key, value = message[1:].split(b':')
                self.storage.store(key, value)
            elif message.startswith(b'r'):
                key = message[1:]
                value = self.storage.retrieve(key)
                client.send_message(value)
            elif message.startswith(b'x'):
                client.close()
                break
        logger.info(f"Connection to {address} closed")
