import socket
import threading
from helpers import unwrap_board

class Network:

    def __init__(self, action_callback, tick_callback):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.2.160"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player, self.board = self.connect()
        self.action_callback = action_callback
        self.tick_callback = tick_callback 

        threading.Thread(target=self.listen_for_data).start()

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = self.client.recv(100*1024*1024)
            print(data)
            return unwrap_board(data.decode())
        except:
            return "Connection failed"

    def send(self, data):
        try:
            message = ','.join(map(str, data))
            self.client.send(message.encode())
        except socket.error as e:
            print(e)


    def listen_for_data(self):
        while True:
            try:
                response = self.client.recv(32).decode()
                if response:
                    data_tuple = tuple(map(int, response.split(',')))
                    if len(data_tuple) == 3:
                        if data_tuple == (0, 0, 0):
                            self.tick_callback()
                        else:
                            self.action_callback(*data_tuple)
                    else:
                        print(f"Unexpected data format: {data_tuple}")
            except socket.error as e:
                print(e)
                break
