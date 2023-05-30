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
                        # time.sleep(0.01 - (datetime.now() - timex))
                    except:
                        pass

                send("!GIVE")
                loop_bool = True
                next_chunk_size = CHUNK_SIZE
                whole_data = {}
                first_write = True

                while loop_bool:
                    try:
                        # if first_write:
                        #     chunk = client.recv(CHUNK_SIZE).decode(FORMAT)
                        # else:
                        #     # print(next_chunk_size)
                        chunk = client.recv(next_chunk_size).decode(FORMAT)
                        print(chunk[:11])
                        if not chunk:
                            print("not chunk")
                            loop_bool = False
                        elif int(chunk[:2]) == int(chunk[3:5]):
                            whole_data[int(chunk[:2])] = chunk[11:]
                            whole_data_string = ""
                            for string in whole_data.values():
                                whole_data_string = whole_data_string + string
                            whole_data_json = json.loads(whole_data_string)
                            print(whole_data_json.keys())
                            print("finished")
                            loop_bool = False
                        elif first_write:
                            for i in range(int(chunk[3:5])):
                                whole_data[i] = ""
                            whole_data[int(chunk[:2])] = chunk[11:]
                            first_write = False
                            next_chunk_size = int(chunk[6:10])
                        else:
                            next_chunk_size = int(chunk[6:10])
                            whole_data[int(chunk[:2])] = chunk[11:]
                    except ValueError:
                        loop_bool=False


                        #     with open("dota_data.json", "w") as fp:
                        #         json.dump(data, fp, indent=4)

            except KeyboardInterrupt:
                print("Interrupting program")
                break


    finally:
        send(DISCONNECT_MESSAGE)
        time.sleep(1)
        print("Disconnecting")
