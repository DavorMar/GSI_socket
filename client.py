import socket
import json
from datetime import datetime, timedelta
import time

HEADER = 5
FORMAT = "utf-8 "
DISCONNECT_MESSAGE = "!DISC"
CHUNK_SIZE = 1211
TEST = False


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)

if __name__ == "__main__":
    ip_inputted = False
    while not ip_inputted:
        ip = input("please input the IP: ")
        port = input("please input the port: ")
        while True:
            correct = input(f"Is your choice correct? [{ip}:{port}] y/n ")
            if correct.lower() == "y":
                ip_inputted = True
                break
            elif correct.lower() == "n":
                break
            else:
                print("wrong input, please respond with y or n")
    # addr = (ip, int(port))
    addr=("192.168.0.14",5050)
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        print("client connected")
        print("Starting data read")
        time.sleep(2)

        while True:
            try:
                send("!GIVE")
                msg_len = client.recv(5).decode(FORMAT)
                msg_len = int(msg_len)
                bytes_recd = 0
                whole_data_string = []
                while bytes_recd < msg_len:
                    chunk = client.recv(min(msg_len - bytes_recd, 1024))
                    if chunk == b'':
                        raise RuntimeError("socket connection broken")
                    whole_data_string.append(chunk)
                    bytes_recd = bytes_recd + len(chunk)
                whole_data_string = b''.join(whole_data_string)
                whole_data_json = json.loads(whole_data_string)
                print(whole_data_json.keys())
                print("finished")

            except ValueError:
                print("value fail")

            except KeyboardInterrupt:
                print("Interrupting program")
                break

    finally:
        send(DISCONNECT_MESSAGE)
        time.sleep(1)
        print("Disconnecting")
