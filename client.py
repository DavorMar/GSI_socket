import socket
import json
from datetime import datetime, timedelta
import time

HEADER = 64
FORMAT = "utf-16"
DISCONNECT_MESSAGE = "!DISCONNECT"
CHUNK_SIZE = 32768 * 2
TEST = True





def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
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

    addr = (ip, int(port))
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        print("client connected")

        print("Starting data read")
        time.sleep(3)

        while True:
            try:
                if TEST:
                    date_chunk = client.recv(CHUNK_SIZE).decode(FORMAT)
                    try:
                        timex = datetime.strptime(date_chunk,'%Y-%m-%d %H:%M:%S.%f')
                        print(datetime.now() - timex)
                        time.sleep(0.01 - (datetime.now() - timex))
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
                        try:
                            data = json.loads(received_data)
                            with open("dota_data.json", "w") as fp:
                                json.dump(data, fp, indent=4)
                            # print(data)
                        except:
                            print("failed first json")
                    received_data += chunk
                        # print(received_data)
            except KeyboardInterrupt:
                print("Interrupting program")
                break


    finally:
        send(DISCONNECT_MESSAGE)
        time.sleep(1)
        print("Disconnecting")
