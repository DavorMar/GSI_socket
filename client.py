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
    # msg_length = len(message)
    # send_length = str(msg_length).encode(FORMAT)
    # send_length += b' ' * (HEADER - len(send_length))
    # client.send(send_length)
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
                loop_bool = True
                next_chunk_size = CHUNK_SIZE
                whole_data = {}
                chunk = client.recv(2).decode(FORMAT)

                for i in range(int(chunk)):
                    whole_data[i] = ""

                for i in range(int(chunk)):
                    chunk2 = client.recv(next_chunk_size).decode(FORMAT)
                    next_chunk_size = int(chunk2[6:10])
                    whole_data[int(chunk2[:2])] = chunk2[11:]
                    print(chunk2[:11])
                    time.sleep(0.0001)

                whole_data_string = ""
                for string in whole_data.values():
                    whole_data_string = whole_data_string + string
                whole_data_json = json.loads(whole_data_string)
                print(whole_data_json.keys())
                print("finished")




                        #     with open("dota_data.json", "w") as fp:
                        #         json.dump(data, fp, indent=4)
            except ValueError:
                print("value fail")
                # while True:
                #     chunkx = client.recv(CHUNK_SIZE).decode(FORMAT)
                #     if not chunkx:
                #         break


            except KeyboardInterrupt:
                print("Interrupting program")
                break


    finally:
        send(DISCONNECT_MESSAGE)
        time.sleep(1)
        print("Disconnecting")
