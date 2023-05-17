import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timedelta
import re



PORT = 5050
# SERVER = '192.168.0.14'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
CHUNK_SIZE = 8192 * 4



class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        now = datetime.now()

        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")

        payload = json.loads(body)
        payload = json.dumps(payload)
        self.server.payload = [payload[i:i + CHUNK_SIZE] for i in range(0, len(payload), CHUNK_SIZE)]
        self.server.payload.append(now.strftime('%Y-%m-%d %H:%M:%S.%f'))
        self.server.running = True
        # print(datetime.now()-now)
        # with open(r"data_sample.json", "w") as fp:
        #     json.dump(payload, fp, indent=4)




class Server(HTTPServer):
    def __init__(self,server_address):
        super(Server, self).__init__(server_address, RequestHandler)
        self.serverx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverx.bind(ADDR)
        self.serverx.setblocking(False)

        self.running = False
        self.payload = []




    def handle_client(self,conn, addr):
        print(f"New connection {addr} connected")
        connected = True
        datas_sent = 0

        while connected:
            try:
                msg = conn.recv(HEADER).decode(FORMAT)

                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"{addr}: disconnected")
            except BlockingIOError as e:
                # Handle the BlockingIOError and continue the loop
                if e.errno != 10035:
                    # Reraise the exception if it's not the expected error
                    raise
            try:
                payload = self.payload[:]
                time_string = payload.pop()
                payload.append("done")
                payload.append(time_string)

                for chunk in payload:
                    conn.send(chunk.encode(FORMAT))
                    time.sleep(0.0001)
                print(datetime.now() - datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S.%f'))
            except BlockingIOError as e:
                if e.errno != 10035:
                    # Reraise the exception if it's not the expected error
                    raise

        conn.close()



    def start(self):
        try:
            gsi_thread = threading.Thread(target=self.serve_forever)
            gsi_thread.start()
            first_time = True
            while not self.running:
                if first_time:
                    print("Dota GSI Server starting..")
                first_time = False
        except:
            print("Could not start server.")
            return
        print("Dota gsi server started, starting sockets now")
        self.serverx.listen()
        print("server is listening on ", SERVER)
        while True:
            try:
                conn, addr = self.serverx.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
            except BlockingIOError as e:
                # Handle the BlockingIOError and continue the loop
                if e.errno != 10035:
                    # Reraise the exception if it's not the expected error
                    raise

def scan_port():
    path = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\cfg\gamestate_integration\gamestate_integration_dota2-gsi.cfg"
    with open(path, "r") as fp:
        read_string = fp.read()

    pattern = r':\d{4,6}'

    try:
        port = int(re.search(pattern, read_string).group()[1:])
        return port
    except AttributeError:
        return 12345678

def prompt_port():
    port = scan_port()
    if port == 12345678:
        print("couldnt scan port in GSI cfg file.")
    else:
        while True:
            answer = input(f"Do you want to use scanned port {port}? y/n ")
            if answer.lower() == "y":
                return port
            elif answer.lower() == "n":
                break
            else:
                print("Please write a y/n answer")
                continue
    while True:
        port = input("Please input the port your GSI config file is set to or your desired port: ")
        try:
            port = int(port)
        except ValueError:
            print("Input a correct port number between 80 and 99999")
            continue
        if port < 80 or port > 99999:
            print("Input a correct port number between 80 and 99999")
        else:
            print(f"Server is starting on port {port}")
            return port



if __name__ == '__main__':
    port = prompt_port()
    server2 = Server(("0.0.0.0", port))
    # app.run(host='0.0.0.0', port=3000)
    print("Server is starting")
    server2.start()