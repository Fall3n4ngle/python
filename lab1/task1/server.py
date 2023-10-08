import socket
import time

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
    
    time.sleep(5)
    print(f"Отримано: {data}")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Час отримання: {current_time}")
    
    success_message = "Дані успішно отримано і оброблено."
    client_socket.send(success_message.encode())

client_socket.close()
server_socket.close()