from socket import socket
from time import sleep


server_socket = socket()
host = "localhost"
port = 1898
server_socket.bind((host, port))
server_socket.listen(5)

client_socket = socket()
client_socket.connect((host, port))


new_client, address = server_socket.accept()

for i in range(10):
    new_client.send(b"Hello!")
    new_client.send(b"World!")
    print(client_socket.recv(4096))

new_client.close()
server_socket.close()
