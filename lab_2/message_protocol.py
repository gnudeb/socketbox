from socket import socket

def recv_message(client_socket: socket):
    message_size = int(client_socket.recv(1))

    buffer = b''
    while len(buffer) < message_size:
        buffer += client_socket.recv(message_size - len(buffer))

    return buffer

s = socket()

host = "localhost"
port = 1898

s.bind((host, port))
s.listen(5)

while True:
    client_socket, address = s.accept()

    message = recv_message(client_socket)
    while len(message) != 0:
        print(message)
        message = recv_message(client_socket)

    client_socket.close()
