import math

PADDLE_WIDTH = 0.02
PADDLE_HEIGHT = 0.2
BALL_WIDTH = 0.01
MAX_ANGLE = math.pi / 3


def calculate_paddle_rebound(ball_y, paddle_y, direction):
    norm_dist_from_centre = (ball_y - paddle_y) / (PADDLE_HEIGHT / 2)  # -1 to 1
    rebound_angle = MAX_ANGLE * math.sin((math.pi * norm_dist_from_centre) / 2)

    new_ball_vel = [direction * math.cos(rebound_angle), math.sin(rebound_angle)]

    return new_ball_vel


class Game:
    def __init__(self):
        self.started = False
        self.game_data = {}
        self.ball = [0.5, 0.5]
        self.ball_vel = [-1, 0]
        self.ball_speed = 0.005

        self.score = [0, 0]

    def move_paddle(self, player_id, request):
        if request == 'DOWN':
            if self.game_data[player_id] + 0.02 + PADDLE_HEIGHT / 2 <= 1:
                self.game_data[player_id] += 0.02
            else:
                self.game_data[player_id] = 1 - PADDLE_HEIGHT / 2
        elif request == 'UP':
            if self.game_data[player_id] - 0.02 - PADDLE_HEIGHT / 2 >= 0:
                self.game_data[player_id] -= 0.02
            else:
                self.game_data[player_id] = PADDLE_HEIGHT / 2

    def reset(self):
        self.ball = [0.5, 0.5]
        self.ball_vel = [-1, 0]
        self.game_data['player1'] = 0.5
        self.game_data['player2'] = 0.5

    def update(self):
        if self.started:
            self.ball[0] += self.ball_vel[0] * self.ball_speed
            self.ball[1] += self.ball_vel[1] * self.ball_speed
            self.game_data["ball"] = self.ball

            if (self.ball[0] - BALL_WIDTH / 2) <= 0.05 + PADDLE_WIDTH / 2:
                if self.game_data['player1'] - PADDLE_HEIGHT / 2 <= self.ball[1] <= self.game_data['player1'] + PADDLE_HEIGHT / 2:
                    self.ball_vel = calculate_paddle_rebound(self.ball[1], self.game_data['player1'], 1)
            if (self.ball[0] + BALL_WIDTH / 2) >= 0.95 - PADDLE_WIDTH / 2:
                if self.game_data['player2'] - PADDLE_HEIGHT / 2 <= self.ball[1] <= self.game_data['player2'] + PADDLE_HEIGHT / 2:
                    self.ball_vel = calculate_paddle_rebound(self.ball[1], self.game_data['player2'], -1)

            if self.ball[1] - BALL_WIDTH / 2 <= 0 or self.ball[1] + BALL_WIDTH / 2 >= 1:
                self.ball_vel[1] *= -1

            if self.ball[0] + BALL_WIDTH / 2 <= 0:
                self.score[0] += 1
                self.reset()
            if self.ball[0] - BALL_WIDTH / 2 >= 1:
                self.score[1] += 1
                self.reset()

            self.game_data['score'] = self.score

