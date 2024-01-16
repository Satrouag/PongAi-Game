import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 3
PADDLE_SPEED = 7
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class PongGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen and caption
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Game")

        # Paddles and ball
        self.player_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 50, 10, 100)
        self.opponent_paddle = pygame.Rect(10, HEIGHT // 2 - 50, 10, 100)
        self.ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        self.ball_speed = [BALL_SPEED, BALL_SPEED]

        # Restart button
        self.restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)

        # Game state
        self.GAME_OVER = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.collidepoint(event.pos):
                    self.reset_game()
                    self.GAME_OVER = False

    def move_paddles(self, keys):
        if keys[pygame.K_UP] and self.opponent_paddle.top > 0:
            self.opponent_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and self.opponent_paddle.bottom < HEIGHT:
            self.opponent_paddle.y += PADDLE_SPEED

        if keys[pygame.K_w] and self.player_paddle.top > 0:
            self.player_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and self.player_paddle.bottom < HEIGHT:
            self.player_paddle.y += PADDLE_SPEED

    def move_ball(self):
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]

        # Ball going off the screen
        if self.ball.right < 0 or self.ball.left > WIDTH:
            self.GAME_OVER = True

        # Ball collision with walls
        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            self.ball_speed[1] = -self.ball_speed[1]

        # Ball collision with paddles
        if self.ball.colliderect(self.player_paddle) or self.ball.colliderect(self.opponent_paddle):
            self.ball_speed[0] = -self.ball_speed[0]

    def draw_objects(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.player_paddle)
        pygame.draw.rect(self.screen, WHITE, self.opponent_paddle)
        pygame.draw.ellipse(self.screen, WHITE, self.ball)

    def draw_restart_button(self):
        # Draw the restart button
        pygame.draw.rect(self.screen, WHITE, self.restart_button)
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, BLACK)
        self.screen.blit(text, (WIDTH // 2 - 35, HEIGHT // 2 + 65))

    def reset_game(self):
        self.ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        self.ball_speed = [BALL_SPEED, BALL_SPEED]

    def run(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            self.handle_events()

            keys = pygame.key.get_pressed()
            self.move_paddles(keys)
            self.move_ball()

            self.draw_objects()
            if self.GAME_OVER:
                self.draw_restart_button()
                pygame.display.flip()
            else:
                pygame.display.flip()

def main():
    pong_game = PongGame()
    pong_game.run()

if __name__ == "__main__":
    main()
