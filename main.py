import pygame
import sys
import time
import math

# Initialize the font module
pygame.font.init()  

# Constants
WIDTH, HEIGHT = 800, 600

TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 24)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

MIDDLE_X = WIDTH // 2
MIDDLE_Y = HEIGHT // 2

class PongGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen and caption
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Game")

        # Create Paddles and ball
        self.player_paddle = pygame.Rect(WIDTH - 20, MIDDLE_Y - 50, 10, 100)
        self.opponent_paddle = pygame.Rect(10, MIDDLE_Y - 50, 10, 100)
        self.ball = pygame.Rect(MIDDLE_X - 15, MIDDLE_Y - 15, 30, 30)
        
        # Define Speeds of objects
        self.ball_spd = 3
        self.ai_speed = 7
        self.paddle_speed = 7
        self.ball_speed = [self.ball_spd, self.ball_spd]

        # Initialize Start time
        self.start_time = time.time()

        # Restart button
        self.restart_button = pygame.Rect(MIDDLE_X - 50, MIDDLE_Y + 30, 100, 50)

        # Mode Buttons
        self.easy_mode_button = pygame.Rect(MIDDLE_X - 50, MIDDLE_Y - 80, 100, 50)
        self.medium_mode_button = pygame.Rect(MIDDLE_X - 50, MIDDLE_Y - 25, 100, 50)
        self.hard_mode_button = pygame.Rect(MIDDLE_X - 50, MIDDLE_Y + 30, 100, 50)

        # Game state
        self.GAME_OVER = False
        self.new_game = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def move_paddles(self, keys):
        # to move the opponents paddles around
        if keys[pygame.K_UP] and self.opponent_paddle.top > 50:
            self.opponent_paddle.y -=self.paddle_speed
        if keys[pygame.K_DOWN] and self.opponent_paddle.bottom < HEIGHT:
            self.opponent_paddle.y +=self.paddle_speed

        # to move the players paddles around
        if keys[pygame.K_w] and self.player_paddle.top > 50:
            self.player_paddle.y -=self.paddle_speed
        if keys[pygame.K_s] and self.player_paddle.bottom < HEIGHT:
            self.player_paddle.y +=self.paddle_speed

    def move_ai_paddle(self):
        # Simple AI strategy: Follow the ball's y-coordinate
        if self.ball.centery < self.opponent_paddle.centery and self.opponent_paddle.top > 50:
            self.opponent_paddle.y -= self.ai_speed
        elif self.ball.centery > self.opponent_paddle.centery and self.opponent_paddle.bottom < HEIGHT:
            self.opponent_paddle.y += self.ai_speed

    def move_ball(self):
        # to move the ball along the direction x and y
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]

        # Ball going off the screen
        if self.ball.right < 0 or self.ball.left > WIDTH:
            self.GAME_OVER = True

        # Ball collision with walls
        if self.ball.top <= 50 or self.ball.bottom >= HEIGHT:
            self.ball_speed[1] = -self.ball_speed[1]

        # Ball collision with paddles
        if self.ball.colliderect(self.player_paddle) or self.ball.colliderect(self.opponent_paddle):
            self.ball_speed[0] = -self.ball_speed[0]
    
    def draw_objects(self):
        # to draw all the objects during the game loop
        self.screen.fill(BLACK)
        self.draw_top_bar(time.time() - self.start_time)
        pygame.draw.rect(self.screen, WHITE, self.player_paddle)
        pygame.draw.rect(self.screen, WHITE, self.opponent_paddle)
        pygame.draw.ellipse(self.screen, WHITE, self.ball)

    def reset_game(self):
        # reset all the required variables
        self.ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        self.new_game = True
        self.GAME_OVER = False
        self.start_time = time.time()

    def draw_top_bar(self, elapsed_time):
        # to draw the top bar during the game loop
        pygame.draw.rect(self.screen, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
        time_label = LABEL_FONT.render(f"Time:{format_time(elapsed_time, True)}", 1, "black")
        score_label = LABEL_FONT.render(f"Score:{format_time(elapsed_time, False)}", 1, "black")

        self.screen.blit(time_label, (5,5))
        self.screen.blit(score_label, (WIDTH -150, 5))

    def draw_start_screen(self):
        # to create and draw all the labels of the starting screen
        self.screen.fill(BLACK)
        head = LABEL_FONT.render("Pong Game", True, WHITE)
        self.screen.blit(head, (MIDDLE_X - 60, 10))

        instructions = LABEL_FONT.render("Use 'W' to move up and Use 'S' to move down your paddle", True,   WHITE)
        self.screen.blit(instructions, (100, 50))

        pygame.draw.rect(self.screen, WHITE, self.easy_mode_button)
        text = LABEL_FONT.render("Easy", True, BLACK)
        self.screen.blit(text, get_middle(self.easy_mode_button))
        
        pygame.draw.rect(self.screen, WHITE, self.medium_mode_button)
        text = LABEL_FONT.render("Medium", True, BLACK)
        self.screen.blit(text, get_middle(self.medium_mode_button))

        pygame.draw.rect(self.screen, WHITE, self.hard_mode_button)
        text = LABEL_FONT.render("Hard", True, BLACK)
        self.screen.blit(text, get_middle(self.hard_mode_button))

        # to update the screen 
        pygame.display.flip()

        # to make sure the start screen is visible untill the user selects a choice
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.easy_mode_button.collidepoint(event.pos):
                        self.ball_spd = 5
                        self.ai_speed = 7
                        self.paddle_speed = 7
                        self.ball_speed = [self.ball_spd, self.ball_spd]
                        run = False
                    elif self.medium_mode_button.collidepoint(event.pos):
                        self.ball_spd = 6
                        self.ai_speed = 7
                        self.paddle_speed = 6
                        self.ball_speed = [self.ball_spd, self.ball_spd]
                        run = False
                    elif self.hard_mode_button.collidepoint(event.pos):
                        self.ball_spd = 7
                        self.ai_speed = 8
                        self.paddle_speed = 5
                        self.ball_speed = [self.ball_spd, self.ball_spd]
                        run = False

    def draw_end_screen(self):
        # similarly creates and display the required labels
        self.screen.fill(BLACK)
        head = LABEL_FONT.render("Game Over", True, WHITE)
        self.screen.blit(head, (get_middle_label(head), 10))

        time_label = LABEL_FONT.render(f"Time Played:{format_time(time.time() - self.start_time, True)}", 1, WHITE)
        self.screen.blit(time_label, (get_middle_label(time_label), MIDDLE_Y - 80))

        score_label = LABEL_FONT.render(f"Your Score:{format_time(time.time() - self.start_time, False)}", 1, WHITE)
        self.screen.blit(score_label, (get_middle_label(score_label), MIDDLE_Y - 30))

        pygame.draw.rect(self.screen, WHITE, self.restart_button)
        text = LABEL_FONT.render("Restart", True, BLACK)
        self.screen.blit(text, get_middle(self.restart_button))

        pygame.display.flip()
        
        # to keep the end screen running untill user choose again
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.collidepoint(event.pos):
                        self.reset_game()
                        run = False

        

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            # to set the frame rate
            clock.tick(60)

            if self.new_game:
                self.draw_start_screen()
                self.new_game = False
                

            self.handle_events()

            keys = pygame.key.get_pressed()
            self.move_paddles(keys)

            # Call the AI paddle movement
            self.move_ai_paddle()  
            self.move_ball()

            self.draw_objects()

            if self.GAME_OVER:
                self.draw_end_screen()
            else:
                pygame.display.flip()

# Some utility functions:- 
def format_time(secs, type):
    # to format the time in desired format
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs %60, 1))
    minutes = int(secs // 60)

    if type:
        return f"{minutes:02d}:{seconds:02d}.{milli}"
    else:
        return seconds
    
def get_middle(surface):
    # to get the middle coordinates of the buttons
    middle_x, middle_y = surface.center
    return (middle_x - 40, middle_y - 20)

def get_middle_label(surface):
    # /to get the middle coordinates of the labels
    return WIDTH / 2 - surface.get_width()/2

def main():
    pong_game = PongGame()
    pong_game.run()

if __name__ == "__main__":
    main()
