import socket
import time
import json
from datetime import datetime, timedelta

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER,PORT)
CHUNK_SIZE = 8192

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
    print((client.recv(2000)))


try:
    print("Starting data read")
    time.sleep(3)
    while True:
        date_chunk = client.recv(CHUNK_SIZE).decode(FORMAT)
        try:
            time = datetime.strptime(date_chunk,'%Y-%m-%d %H:%M:%S.%f')
            print(datetime.now() - time)
        except:
            pass

        received_data = ""
        loop_bool = True
        while loop_bool:
            chunk = client.recv(CHUNK_SIZE).decode(FORMAT)
            if not chunk:
                print("not chunk")
                loop_bool = False
            elif chunk in ["done", " done"]:
                loop_bool = False
            received_data += chunk
                # print(received_data)


finally:
    send(DISCONNECT_MESSAGE)
    print("Disconnecting")