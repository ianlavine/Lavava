import socket
import threading
from constants import *

class Network:
    def __init__(self, action_callback, tick_callback, eliminate_callback, reset_game_callback):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = None
        self.port = 5555
        self.action_callback = action_callback
        self.tick_callback = tick_callback
        self.eliminate_callback = eliminate_callback
        self.reset_game_callback = reset_game_callback

        self.get_user_input_and_connect()

    def get_user_input_and_connect(self):
        while True:
            self.get_user_input_for_game()
            if self.connect_and_receive_board():
                threading.Thread(target=self.listen_for_data).start()
                break

    def get_user_input_for_game(self):
        self.server = input("Input Server IP Address: ")
        self.addr = (self.server, self.port)
        while True:
            user_input = input("Do you want to HOST or JOIN a game? (HOST/JOIN): ").strip().upper()
            if user_input in ["HOST", "JOIN"]:
                break
            else:
                print("Invalid input. Please enter 'HOST' or 'JOIN'.")

        if user_input == "HOST":
            player_count = input("Enter the number of players for the game: ")
            self.init_data = f"HOST,{player_count}"
        else:
            game_code = input("Enter the game code to join: ")
            self.init_data = f"JOIN,{game_code}"

    def connect_and_receive_board(self):
        if self.establish_connection():
            return self.receive_board_data()

    def establish_connection(self):
        try:
            self.client.connect(self.addr)
            self.client.send(self.init_data.encode())
            data = self.client.recv(1024)
            response = data.decode()
            if response == "INVALID_CODE":
                print("Failed to join the game: Invalid game code.")
                return False
            else:
                print("Connected to game", response)
                return True
        except:
            print("Connection failed.")
            return False

    def receive_board_data(self):
        try:
            data = self.client.recv(1024)
            self.data = data.decode()
            return True
        except:
            print("Failed to receive board data.")
            return False

    def send(self, data):
        try:
            message = ','.join(map(str, data)) + ','
            self.client.send(message.encode())
        except socket.error as e:
            print(e)

    def listen_for_data(self):
        while True:
            try:
                response = self.client.recv(32).decode()
                if response:
                    data_list = list(filter(None, response.split(',')))
                    data_tuple = tuple(map(int, data_list))
                    while len(data_tuple) >= 3:
                        sub = data_tuple[:3]
                        data_tuple = data_tuple[3:]
                        if sub == (0, 0, 0):
                            self.tick_callback()
                        elif sub[0] == -1:
                            print("Player", sub[1], "has been eliminated.")
                            self.eliminate_callback(sub[1])
                        elif sub[0] == -2:
                            print("Player", sub[1], "has won the game!")
                            self.reset_game_callback()
                        else:
                            print(sub)
                            self.action_callback(*sub)
            except socket.error as e:
                print(e)
                break

if __name__ == "__main__":
    # replace with your actual callbacks
    def action_callback(): pass 
    def tick_callback(): pass 

    Network(action_callback, tick_callback)
