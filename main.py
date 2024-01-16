import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 3
PADDLE_SPEED = 7

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Create the paddles and ball
player_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 50, 10, 100)
opponent_paddle = pygame.Rect(10, HEIGHT // 2 - 50, 10, 100)
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Create the restart button
restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the restart button
            if restart_button.collidepoint(event.pos):
                ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
                ball_speed = [BALL_SPEED, BALL_SPEED]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and opponent_paddle.top > 0:
        opponent_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and opponent_paddle.bottom < HEIGHT:
        opponent_paddle.y += PADDLE_SPEED

    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball going off the screen
    if ball.right < 0 or ball.left > WIDTH:
        # Reset the ball position to the center
        # Draw the restart button
        pygame.draw.rect(screen, WHITE, restart_button)
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 35, HEIGHT // 2 + 65))
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed[0] = -ball_speed[0]

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    pygame.time.Clock().tick(60)
