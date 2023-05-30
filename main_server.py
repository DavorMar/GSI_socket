import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timedelta


HEADER = 5
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISC"
CHUNK_SIZE = 1200
TEST = False




class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        now = datetime.now()
        # print(self.client_address)
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")
        payload = json.loads(body)
        payload = self.filter_json(payload)
        payload = json.dumps(payload)
        # print(len(payload))
        # print(payload)
        self.server.payload = [payload[i:i + CHUNK_SIZE] for i in range(0, len(payload), CHUNK_SIZE)]
        # print(len(self.server.payload))
        self.server.running = True
        if TEST:
            self.server.payload.append(now.strftime('%Y-%m-%d %H:%M:%S.%f'))
        time.sleep(5)

    def filter_json(self, payload):
        if len(payload["buildings"]["radiant"].keys()) < 2:
            draft = True
        else:
            draft = False
        if draft:
            new_payload = {
                "draft_state": draft,
                "draft": {}
            }
            new_payload['draft'] = payload['draft']
        else:
            new_payload = {
                "draft_state": draft,
                "map": {},
                "players": {},
                "draft":{}
            }
            new_payload["map"]['game_time'] = payload['map']['game_time']
            new_payload["map"]['matchid'] = payload['map']['matchid']
            new_payload["map"]['clock_time'] = payload['map']['clock_time']
            new_payload["map"]['radiant_score'] = payload['map']['radiant_score']
            new_payload["map"]['dire_score'] = payload['map']['dire_score']
            new_payload["map"]['game_state'] = payload['map']['game_state']
            new_payload["map"]['win_team'] = payload['map']['win_team']
            new_payload["map"]['roshan_state'] = payload['map']['roshan_state']
            new_payload["map"]['roshan_state_end_seconds'] = payload['map']['roshan_state_end_seconds']
            for team in payload['player']:
                for player in payload['player'][team]:
                    new_payload['players'][player] = {}
                    new_payload['players'][player]['steamid'] = payload['player'][team][player]['steamid']
                    new_payload['players'][player]['accountid'] = payload['player'][team][player]['accountid']

                    new_payload['players'][player]['name'] = payload['player'][team][player]['name']
                    new_payload['players'][player]['kills'] = payload['player'][team][player]['kills']
                    new_payload['players'][player]['deaths'] = payload['player'][team][player]['deaths']
                    new_payload['players'][player]['assists'] = payload['player'][team][player]['assists']
                    new_payload['players'][player]['last_hits'] = payload['player'][team][player]['last_hits']
                    new_payload['players'][player]['denies'] = payload['player'][team][player]['denies']
                    new_payload['players'][player]['team_name'] = payload['player'][team][player]['team_name']
                    new_payload['players'][player]['player_slot'] = payload['player'][team][player]['player_slot']
                    new_payload['players'][player]['team_slot'] = payload['player'][team][player]['team_slot']
                    new_payload['players'][player]['net_worth'] = payload['player'][team][player]['net_worth']
                    new_payload['players'][player]['gpm'] = payload['player'][team][player]['gpm']
                    new_payload['players'][player]['xpm'] = payload['player'][team][player]['xpm']
                    new_payload['players'][player]['wards_purchased'] = payload['player'][team][player]['wards_purchased']
                    new_payload['players'][player]['wards_placed'] = payload['player'][team][player]['wards_placed']
                    new_payload['players'][player]['wards_destroyed'] = payload['player'][team][player]['wards_destroyed']
                    new_payload['players'][player]['runes_activated'] = payload['player'][team][player]['runes_activated']
            for team in payload['hero']:
                for player in payload['hero'][team]:
                    new_payload['players'][player]['id'] = payload['hero'][team][player]['id']
                    new_payload['players'][player]['hero_name'] = payload['hero'][team][player]['name']
                    new_payload['players'][player]['level'] = payload['hero'][team][player]['level']
                    new_payload['players'][player]['aghanims_scepter'] = payload['hero'][team][player]['aghanims_scepter']
                    new_payload['players'][player]['aghanims_shard'] = payload['hero'][team][player]['aghanims_shard']
                    new_payload['players'][player]['alive'] = payload['hero'][team][player]['alive']
            for team in payload['items']:
                for player in payload['items'][team]:
                    new_payload['players'][player]['slot0'] = payload['items'][team][player]['slot0']["name"]
                    new_payload['players'][player]['slot1'] = payload['items'][team][player]['slot1']["name"]
                    new_payload['players'][player]['slot2'] = payload['items'][team][player]['slot2']["name"]
                    new_payload['players'][player]['slot3'] = payload['items'][team][player]['slot3']["name"]
                    new_payload['players'][player]['slot4'] = payload['items'][team][player]['slot4']["name"]
                    new_payload['players'][player]['slot5'] = payload['items'][team][player]['slot5']["name"]
                    new_payload['players'][player]['slot6'] = payload['items'][team][player]['slot6']["name"]
                    new_payload['players'][player]['slot7'] = payload['items'][team][player]['slot7']["name"]
                    new_payload['players'][player]['slot8'] = payload['items'][team][player]['slot8']["name"]
            return new_payload







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
                elif msg == "!GIVE":
                    self.send_data(conn)

            except BlockingIOError as e:

                # Handle the BlockingIOError and continue the loop
                if e.errno != 10035:
                    # Reraise the exception if it's not the expected error
                    raise
    def send_data(self,conn):
            try:
                payload = self.payload[:]
                x = 0
                conn.send(str(len(payload)).zfill(2).encode(FORMAT))
                for chunk in payload:
                    if x == len(payload) - 1:
                        print("last packet")
                        new_chunk = f"{str(x).zfill(2)}|{str(len(payload) - 1).zfill(2)}+{str(11).zfill(4)}+{chunk}"
                    else:
                        new_chunk = f"{str(x).zfill(2)}|{str(len(payload)-1).zfill(2)}+{str(len(payload[x+1])+11).zfill(4)}+{chunk}"
                    conn.send(new_chunk.encode(FORMAT))

                    time.sleep(0.0000001)
                    if x == len(payload) - 1:
                        print(f"{str(x).zfill(2)}|{str(len(payload)-1).zfill(2)}+{str(11).zfill(4)}")
                    else:
                        print(f"{str(x).zfill(2)}|{str(len(payload)-1).zfill(2)}+{str(len(payload[x+1])+11).zfill(4)}", len(new_chunk.encode(FORMAT)))
                    x += 1

            except BlockingIOError as e:
                print("blocking error")
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




