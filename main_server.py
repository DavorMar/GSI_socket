import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json



PORT = 5050
# SERVER = '192.168.0.14'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"



class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")
        print(len(body))
        payload = json.loads(body)
        # print(payload)
        self.server.payload = payload
        self.server.running = True
        # with open(r"data_sample.json", "w") as fp:
        #     json.dump(payload, fp, indent=4)




class Server(HTTPServer):
    def __init__(self,server_address):
        super(Server, self).__init__(server_address, RequestHandler)
        self.serverx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverx.bind(ADDR)
        self.serverx.setblocking(False)

        self.running = False
        self.payload = ""



    def handle_client(self,conn, addr):
        print(f"New connection {addr} connected")
        connected = True
        datas_sent = 0
        while connected:
            try:
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                        print(f"{addr}: disconnected")
            except BlockingIOError as e:
                # Handle the BlockingIOError and continue the loop
                if e.errno != 10035:
                    # Reraise the exception if it's not the expected error
                    raise
            try:

                conn.send(json.dumps(self.payload).encode(FORMAT))
                print("sent_data ", datas_sent)
                datas_sent += 1
            except:
                # print("failed_send")
                pass
        conn.close()



    def start(self):
        try:
            threa = threading.Thread(target=self.serve_forever)
            threa.start()
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




if __name__ == '__main__':
    server2 = Server(("0.0.0.0", 3000))
    # app.run(host='0.0.0.0', port=3000)
    print("Server is starting")
    server2.start()