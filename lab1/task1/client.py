import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)
client_socket.connect(server_address)

message = input("Введіть текст для відправки на сервер: ")
client_socket.send(message.encode())

client_socket.close()