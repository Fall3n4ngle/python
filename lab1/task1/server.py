import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)
server_socket.bind(server_address)

server_socket.listen(1)
print("Сервер готовий приймати з'єднання...")

client_socket, client_address = server_socket.accept()
print(f"З'єднання з {client_address} успішно встановлено.")

while True:
    data = client_socket.recv(1024).decode()
    if not data:
        break
    print(f"Отримано: {data}")

    if data == "exit":
        break

client_socket.close()
server_socket.close()