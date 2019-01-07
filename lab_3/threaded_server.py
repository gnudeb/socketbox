from socket import socket
from threading import Thread

def handle_connection(client_socket: socket):
    client_socket.send(b"Hello, World!\r\n")
    client_socket.close()

s = socket()

host = "localhost"
port = 1898

s.bind((host, port))
s.listen(5)

while True:
    client_socket, address = s.accept()
    client_thread = Thread(target=handle_connection, args=(client_socket,))
    client_thread.start()
