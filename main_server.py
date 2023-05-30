import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timedelta


HEADER = 64
FORMAT = "utf-16"
DISCONNECT_MESSAGE = "!DISCONNECT"
CHUNK_SIZE = 32768 * 2
TEST = True




class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        now = datetime.now()
        # print(self.client_address)
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")
        payload = json.loads(body)
        # if 'map' in payload.keys():
        #     print(len(json.dumps(payload)), payload['draft'], payload['map']['clock_time'], payload['map']['game_state'], payload['map']['win_team'],payload['auth'])
        # else:
        #     print(payload)
        payload = json.dumps(payload)
        self.server.payload = [payload[i:i + CHUNK_SIZE] for i in range(0, len(payload), CHUNK_SIZE)]
        # print(len(self.server.payload))
        self.server.running = True
        if TEST:
            self.server.payload.append(now.strftime('%Y-%m-%d %H:%M:%S.%f'))



class Server(HTTPServer):
    def __init__(self,server_address, socket_port):
        super(Server, self).__init__(server_address, RequestHandler)
        self.serverx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.ip_addr = socket.gethostbyname(socket.gethostname())
        self.ip_addr = "192.168.0.14"
        addr = (self.ip_addr, socket_port)
        self.serverx.bind(addr)
        self.serverx.setblocking(False)
        self.running = False
        self.payload = []
        self.exit_flag = False





    def handle_client(self,conn, addr):
        print(f"New connection {addr} connected")
        while not self.exit_flag:
            try:
                msg = conn.recv(HEADER).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    print(f"{addr}: disconnected")
                    break

            except BlockingIOError as e:
                # Handle the BlockingIOError and continue the loop
                if e.errno != 10035:
                    # Reraise the exception if it's not the expected error
                    raise

            try:

                payload = self.payload[:]

                if TEST:
                    time_string = payload.pop()
                payload.append("done")
                if TEST:
                    payload.append(time_string)
                print(len(payload), len(payload[0]))
                for chunk in payload:
                    conn.send(chunk.encode(FORMAT))
                    time.sleep(0.0001)

            except BlockingIOError as e:
                if e.errno != 10035:
                    # Reraise the exception if it's not the expected error
                    raise
            except (ConnectionResetError, ConnectionAbortedError):
                print("possible disconnect")

        conn.close()

    def start(self):
        try:
            self.gsi_thread = threading.Thread(target=self.serve_forever)
            self.gsi_thread.start()
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
        print("server is listening on ", self.ip_addr )
        while not self.exit_flag:
            try:
                conn, addr = self.serverx.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
            except BlockingIOError as e:
                # Handle the BlockingIOError and continue the loop
                if e.errno != 10035:
                    # Reraise the exception if it's not the expected error
                    raise




