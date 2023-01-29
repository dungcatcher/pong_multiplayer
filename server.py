import socket
from threading import Thread

HOST = "10.0.0.105"
PORT = 65432


class GameServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        print('Server has started, waiting for clients...')
        self.connected_clients = []

        self.paddle1_pos = 0.5

        self.check_connections()

    def handle_client(self, client_socket, addr):
        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            print(f'{addr} >> {msg}')

            if msg == b'UP':
                self.paddle1_pos += 0.01
                string_pos = str(self.paddle1_pos)
                client_socket.send(str.encode(string_pos))
            # client_socket.send(msg)

    def check_connections(self):
        self.socket.listen()
        while True:
            conn, addr = self.socket.accept()
            self.connected_clients.append((conn, addr))
            client_thread = Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()
            client_thread.join()


game_server = GameServer()

