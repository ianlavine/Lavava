import socket
from _thread import start_new_thread
from queue import Queue
from game import Game
import sys
import time
from threading import Thread
from constants import *
import random
import string

class Server:
    def __init__(self, port):
        self.server = '0.0.0.0'
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting_players = {}  # Stores the waiting players with the game code as the key
        self.games = {}  # Stores the active games with the game code as the key

        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
            sys.exit()

        self.s.listen(10)
        print("Waiting for a connection, Server Started")

    def generate_game_code(self):
        """Generate a unique game code."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def send_ticks(self, game):
        time.sleep(1)
        tick_message = "0,0,0,"
        while True:
            for i, connection in enumerate(game.connections):
                try:
                    connection.sendall(tick_message.encode())
                except OSError as e:
                    print(f"Error on connection {i}: {e}")
                    del game.connections[i]
            time.sleep(0.1)

    def threaded_client(self, conn):
        data = conn.recv(1024).decode()
        is_host, player_count_or_code = data.split(",")
        print(is_host, player_count_or_code)

        if is_host == "HOST":
            player_count = int(player_count_or_code)
            game_code = self.generate_game_code() # Generate a unique game code for the new game
            self.waiting_players[game_code] = {"player_count": player_count, "players": [conn]}
            conn.sendall(game_code.encode())
        elif is_host == "JOIN":
            if player_count_or_code in self.waiting_players:
                conn.sendall(player_count_or_code.encode())
                self.waiting_players[player_count_or_code]["players"].append(conn)
                
                if len(self.waiting_players[player_count_or_code]["players"]) == self.waiting_players[player_count_or_code]["player_count"]:
                    game = Game()
                    game.connections = self.waiting_players.pop(player_count_or_code)["players"]
                    self.start_game(game, player_count_or_code)
            else:
                conn.sendall("INVALID_CODE".encode())

    def start_game(self, game, game_code):
        tick_thread = Thread(target=self.send_ticks, args=(game,))
        tick_thread.daemon = True
        tick_thread.start()

        for i, conn in enumerate(game.connections):
            start_new_thread(self.threaded_client_in_game, (i, conn, game))

    def threaded_client_in_game(self, player, conn, game):
        conn.send(game.graph.repr(player).encode())
        while True:
            try:
                data = conn.recv(32)
                if not data:
                    print("Disconnected")
                    break
                else:
                    print("Received: ", data.decode())
                    for connection in game.connections:
                        connection.sendall(data)
            except socket.error as e:
                print(e)
        
        print("Lost connection")
        conn.close()

    def run(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            
            start_new_thread(self.threaded_client, (conn,))

if __name__ == "__main__":
    server = Server(5555)
    server.run()
