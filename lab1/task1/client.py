import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)
client_socket.connect(server_address)

while True:
    message = input("Введіть текст для відправки на сервер (або 'exit' для закриття): ")

    client_socket.send(message.encode())

    if message == "exit":
        break

client_socket.close()