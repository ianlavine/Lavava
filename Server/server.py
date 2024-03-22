import socket
from _thread import start_new_thread
from threading import Thread
from batch import Batch
import sys
import time
import json

class Server:
    def __init__(self, port):
        self.server = "0.0.0.0"
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting_players = (
            None  # Stores the waiting players with the game code as the key
        )
        self.games = {}  # Stores the active games with the game code as the key

        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
            sys.exit()

        self.s.listen(10)
        print("Waiting for a connection, Server Started")

    def send_ticks(self, batch):
        time.sleep(1)
        while True:
            for i, connection in enumerate(batch.connections):
                try:
                    connection.sendall(batch.tick_json(i).encode())
                except OSError as e:
                    print(f"Error on connection {i}: {e}")
                    del batch.connections[i]
            time.sleep(0.1)

    def threaded_client(self, conn):

        data = conn.recv(1024).decode()
        json_data = json.loads(data)
        is_host = json_data["type"]
        player_count = json_data["players"]
        mode = json_data["mode"]

        if is_host == "HOST":
            player_count = int(player_count)
            self.waiting_players = Batch(player_count, mode, conn)
            conn.sendall("Players may JOIN".encode())
        elif is_host == "JOIN":
            if self.waiting_players:
                conn.sendall("JOINED".encode())
                self.waiting_players.add_player(conn)

                if self.waiting_players.is_ready():
                    print("Game is ready to start")
                    self.waiting_players.build()
                    self.start_game(self.waiting_players)
                else:
                    print("Game is not ready to start")
            else:
                conn.sendall("FAIL".encode())

    def start_game(self, batch):

        tick_thread = Thread(target=self.send_ticks, args=(game,))
        tick_thread.daemon = True
        tick_thread.start()

        for i, conn in enumerate(batch.connections):
            start_new_thread(self.threaded_client_in_game, (i, conn, batch))

    def threaded_client_in_game(self, player, conn, batch):
        conn.send(batch.repr(player).encode())
        print("Sent start data to player")
        while True:
            try:
                data = json.loads(conn.recv(1000).decode())
                if not data:
                    print("Disconnected")
                    break
                else:

                    print("Received: ", data.decode())
                    # for connection in batch.connections:
                    #     connection.sendall(data)
                    if message := batch.process(player, data):
                        self.problem(conn, message)
            except socket.error as e:
                print(e)

        print("Lost connection")
        conn.close()

    def problem(self, conn, message="Problem"):
        conn.send(json.dumps({"COB": message}).encode())

    def run(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            start_new_thread(self.threaded_client, (conn,))


server = Server(5555)
server.run()