import socket
import time
import json

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print("client connected")


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print((client.recv(4096*12)))


try:
    print("Starting data read")
    while True:
        print(len(client.recv(4096*40).decode(FORMAT)))
        data = json.loads(client.recv(4096*40).decode(FORMAT))
finally:
    send(DISCONNECT_MESSAGE)
    print("Disconnecting")