import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timedelta


HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
CHUNK_SIZE = 32768
TEST = True


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        now = datetime.now()
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")
        payload = json.loads(body)
        payload = json.dumps(payload)
        self.server.payload = [payload[i:i + CHUNK_SIZE] for i in range(0, len(payload), CHUNK_SIZE)]
        if TEST:
            self.server.payload.append(now.strftime('%Y-%m-%d %H:%M:%S.%f'))
            self.server.running = True


class Server(HTTPServer):
    def __init__(self,server_address, socket_port):
        super(Server, self).__init__(server_address, RequestHandler)
        self.serverx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_addr = socket.gethostbyname(socket.gethostname())
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
                for chunk in payload:
                    conn.send(chunk.encode(FORMAT))
                    time.sleep(0.0001)
                print(datetime.now() - datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S.%f'))
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




