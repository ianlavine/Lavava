import socket
from _thread import start_new_thread
import pickle
from queue import Queue
from game import Game
import sys

class Server:
    def __init__(self, ip, port):
        self.server = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting_players = Queue()

        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
            sys.exit()

        self.s.listen(10)
        print("Waiting for a connection, Server Started")

    def threaded_client(self, player, game):
        game.connections[player].send(pickle.dumps((player, game.board)))
        while True:
            try:
                data = game.connections[player].recv(32)
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
        game.connections[player].close()

    def run(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            
            self.waiting_players.put(conn)
            if self.waiting_players.qsize() == 2:
                game = Game()
                game.add_player(self.waiting_players.get())
                game.add_player(self.waiting_players.get())
                start_new_thread(self.threaded_client, (0, game))
                start_new_thread(self.threaded_client, (1, game))

if __name__ == "__main__":
    server = Server("192.168.9.109", 5555)
    server.run()