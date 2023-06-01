import socket
import json
from datetime import datetime, timedelta
import time

HEADER = 5
FORMAT = "utf-8 "
DISCONNECT_MESSAGE = "!DISC"
CHUNK_SIZE = 1024
TEST = False
TIME_SLEEPING = 0.05


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)

def print_loading(i):
    if i % 40 == 0:
        print("\r Fetching data | ", end="")
    elif i % 40 == 10:
        print("\r Fetching data / ", end="")
    elif i % 40 == 20:
        print("\r Fetching data - ", end="")
    elif i % 40 == 30:
        print("\r Fetching data \ ", end="")

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
        print(f"client connected to {addr[0]}, {addr[1]}")
        print("Starting data read")
        time.sleep(2)
        counter = 0
        while True:
            print_loading(counter)
            counter += 1
            if counter == 120:
                counter = 0
            try:
                time.sleep(TIME_SLEEPING)
                send("!GIVE")
                msg_len = client.recv(HEADER).decode(FORMAT)
                msg_len = int(msg_len)
                bytes_recd = 0
                whole_data_string = []
                while bytes_recd < msg_len:
                    chunk = client.recv(min(msg_len - bytes_recd, CHUNK_SIZE))
                    if chunk == b'':
                        raise RuntimeError("\nsocket connection broken")
                    whole_data_string.append(chunk)
                    bytes_recd = bytes_recd + len(chunk)
                whole_data_string = b''.join(whole_data_string)
                whole_data_json = json.loads(whole_data_string)

                if whole_data_json["game_state"]:
                    with open("gsi_data.json", "w") as fp:
                        json.dump(whole_data_json, fp=fp, indent=4)

            except ValueError:
                print("\nvalue fail")

            except KeyboardInterrupt:
                print("\nInterrupting program")
                break
    finally:
        send(DISCONNECT_MESSAGE)
        time.sleep(1)
        print("Disconnecting")