import socket 
import threading

nickname = input("Choose a nickname")

host = "127.0.0.1"
port = 44444

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def recv():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occurred")
            client.close()
            break

def send():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode("ascii"))

receiveThread = threading.Thread(target=recv)
receiveThread.start()

sendThred = threading.Thread(target=send)
sendThred.start()