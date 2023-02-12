import pygame
import socket
import json
from threading import Thread
import pygame.freetype

pygame.init()

HOST = "10.0.0.105"
PORT = 65432


class GameClient:
    def __init__(self):
        self.window = pygame.display.set_mode((960, 540))
        self.clock = pygame.time.Clock()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.player_id = None
        self.player_paddles = {}

        self.started = False
        self.queueing_font = pygame.freetype.SysFont('ebrima', 32)

        connection_thread = Thread(target=self.connect_with_server, daemon=True)
        connection_thread.start()

    def connect_with_server(self):
        self.socket.connect((HOST, PORT))
        self.player_id = self.get_response()

        while True:
            response = self.get_response()
            if not response:
                break
            else:
                server_response = self.get_response()
                print(server_response)
                self.player_paddles = json.loads(server_response)

    def get_response(self):
        response = self.socket.recv(1024)
        decoded_response = response.decode('utf-8')
        return decoded_response

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def send_data_to_server(self, data):
        self.socket.sendall(data.encode())

    def update(self):
        self.clock.tick(60)

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_UP] or key_input[pygame.K_DOWN]:
            if key_input[pygame.K_UP]:
                self.send_data_to_server("UP")
            elif key_input[pygame.K_DOWN]:
                self.send_data_to_server("DOWN")

        self.draw()

        pygame.display.update()

    def draw(self):
        self.window.fill((30, 30, 30))

        if self.player_paddles != {}:
            for key, value in self.player_paddles.items():
                if key == "player1" or key == "player2":
                    if key == "player1":
                        x_value = 0.05
                    else:
                        x_value = 0.95
                    rect = pygame.Rect(0, 0, 0.02 * self.window.get_width(), 0.2 * self.window.get_height())
                    rect.center = (x_value * self.window.get_width(), value * self.window.get_height())
                    pygame.draw.rect(self.window, (255, 255, 255), rect)
                elif key == "ball":
                    pygame.draw.circle(self.window, (255, 255, 255),
                                       (value[0] * self.window.get_width(),
                                        value[1] * self.window.get_height()), 0.01 * self.window.get_width())
                elif key == "score":
                    p1_score_surf, p1_score_rect = self.queueing_font.render(f'{value[0]}', (255, 255, 255))
                    p1_score_rect.center = (self.window.get_width() / 4, 0.1 * self.window.get_height())
                    self.window.blit(p1_score_surf, p1_score_rect)

                    p2_score_surf, p2_score_rect = self.queueing_font.render(f'{value[1]}', (255, 255, 255))
                    p2_score_rect.center = (3 * self.window.get_width() / 4, 0.1 * self.window.get_height())
                    self.window.blit(p2_score_surf, p2_score_rect)
        else:
            queue_surf, queue_rect = self.queueing_font.render('Queueing...', (255, 255, 255))
            queue_rect.center = self.window.get_width() / 2, self.window.get_height() / 2
            self.window.blit(queue_surf, queue_rect)


game_client = GameClient()

while True:
    game_client.handle_events()
    game_client.update()
