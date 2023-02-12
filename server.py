import socket
from threading import Thread
import json
from game import Game
import pygame
import pickle

HOST = "10.0.0.105"
PORT = 65432


class GameServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        print('Server has started, waiting for clients...')

        self.game = Game()
        self.clients = set()

        self.clock = pygame.time.Clock()

        self.sent_start_msg = False

        connections_thread = Thread(target=self.check_connections)
        connections_thread.start()

        self.update()

        connections_thread.join()

    def update(self):
        while True:
            if self.game.started:
                self.clock.tick(120)
                self.game.update()
                serialised_player_paddles = json.dumps(self.game.game_data)
                for client in self.clients:
                    client.send(serialised_player_paddles.encode('utf-8'))

    def handle_client(self, client_socket, addr):
        self.clients.add(client_socket)

        player_id = f'player{len(self.clients)}'
        client_socket.send(player_id.encode('utf-8'))
        self.game.game_data[player_id] = 0.5

        while True:
            if len(self.clients) == 2:
                self.game.started = True
            if self.game.started:
                self.clock.tick(120)
                if not self.sent_start_msg:
                    serialised_player_paddles = json.dumps(self.game.game_data)
                    for client in self.clients:
                        client.sendall(serialised_player_paddles.encode())
                    self.sent_start_msg = True

                msg = client_socket.recv(1024)
                if not msg:
                    break
                else:
                    msg = msg.decode()
                    print(f'{addr} >> {msg}')

                    if msg == 'UP':
                        self.game.move_paddle(player_id, 'UP')
                    if msg == 'DOWN':
                        self.game.move_paddle(player_id, 'DOWN')

        for client in self.clients:
            client.close()
        self.clients = set()

    def check_connections(self):
        self.socket.listen()
        while True:
            conn, addr = self.socket.accept()
            print(f'{addr} has connected!')
            client_thread = Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()


game_server = GameServer()

