import socket
from threading import Thread
import json
import pickle

HOST = "10.0.0.105"
PORT = 65432


class GameServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        print('Server has started, waiting for clients...')

        self.player_paddles = {}
        self.clients = set()

        self.check_connections()

    def handle_client(self, client_socket, addr):
        self.player_paddles[addr[0]] = 0.5
        self.clients.add(client_socket)

        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            else:
                msg = msg.decode()
                print(f'{addr} >> {msg}')

                if msg == 'UP':
                    self.player_paddles[addr[0]] += 0.01
                if msg == 'DOWN':
                    self.player_paddles[addr[0]] -= 0.01

                serialised_player_paddles = json.dumps(self.player_paddles)
                for client in self.clients:
                    client.sendall(serialised_player_paddles.encode())

    def check_connections(self):
        self.socket.listen()
        while True:
            conn, addr = self.socket.accept()
            print(f'{addr} has connected!')
            client_thread = Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()


game_server = GameServer()

