import pygame
import socket

HOST = "10.0.0.105"
PORT = 65432


class GameClient:
    def __init__(self):
        self.window = pygame.display.set_mode((960, 540))
        self.clock = pygame.time.Clock()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect_with_server()

    def connect_with_server(self):
        self.socket.connect((HOST, PORT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def send_data_to_server(self, data):
        self.socket.sendall(data.encode())
        result = self.socket.recv(1024)
        print(result)

    def update(self):
        self.clock.tick(60)

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_UP]:
            self.send_data_to_server("UP")
        elif key_input[pygame.K_DOWN]:
            self.send_data_to_server("DOWN")

        self.draw()

        pygame.display.update()

    def draw(self):
        self.window.fill((30, 30, 30))


game_client = GameClient()

while True:
    game_client.handle_events()
    game_client.update()
