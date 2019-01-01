from socket import socket

s = socket()

host = "localhost"
port = 1898

s.bind((host, port))
s.listen(5)

while True:
    client_socket, address = s.accept()
    client_socket.send(b"Hello, World!\r\n")
    client_socket.close()
