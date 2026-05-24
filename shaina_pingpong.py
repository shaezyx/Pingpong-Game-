import pygame
import random

# Initialize
pygame.init()

# Screen
WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shaina Tutor Ping Pong")

# Colors
YELLOW = (255, 230, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NEON = (57, 255, 20)

# Fonts
title_font = pygame.font.SysFont("Arial", 55)
font = pygame.font.SysFont("Arial", 35)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Paddle
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 120
PADDLE_SPEED = 8

# Ball
BALL_SIZE = 22
ball_speed_x = 6
ball_speed_y = 6
speed_boost = 0.5

# Scores
shaina_score = 0
player2_score = 0
MAX_SCORE = 5

# Paddles
left_paddle = pygame.Rect(
    40,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

right_paddle = pygame.Rect(
    WIDTH - 55,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

# Ball
ball = pygame.Rect(
    WIDTH // 2,
    HEIGHT // 2,
    BALL_SIZE,
    BALL_SIZE
)

# Buttons
start_button = pygame.Rect(WIDTH // 2 - 140, 260, 280, 80)
restart_button = pygame.Rect(WIDTH // 2 - 160, 360, 320, 80)

# States
game_started = False
game_over = False
winner = ""

# Reset Ball
def reset_ball():
    global ball_speed_x, ball_speed_y

    ball.center = (WIDTH // 2, HEIGHT // 2)

    ball_speed_x = random.choice([-6, 6])
    ball_speed_y = random.choice([-6, 6])

# Main Loop
running = True

while running:

    clock.tick(FPS)

    screen.fill(YELLOW)

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Start
            if not game_started and start_button.collidepoint(event.pos):

                game_started = True
                game_over = False

                shaina_score = 0
                player2_score = 0

                reset_ball()

            # Restart
            if game_over and restart_button.collidepoint(event.pos):

                game_started = False
                game_over = False

                shaina_score = 0
                player2_score = 0

                reset_ball()

    # START SCREEN
    if not game_started:

        title = title_font.render("SHAINA TUTOR PING PONG", True, RED)

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 150)
        )

        pygame.draw.rect(
            screen,
            RED,
            start_button,
            border_radius=20
        )

        start_text = font.render("START GAME", True, WHITE)

        screen.blit(
            start_text,
            (
                start_button.x + start_button.width // 2 - start_text.get_width() // 2,
                start_button.y + 20
            )
        )

        controls = font.render(
            "W/S = Shaina | UP/DOWN = Player 2",
            True,
            BLACK
        )

        screen.blit(
            controls,
            (WIDTH // 2 - controls.get_width() // 2, 500)
        )

    # GAME OVER SCREEN
    elif game_over:

        winner_text = title_font.render(winner, True, NEON)

        screen.blit(
            winner_text,
            (WIDTH // 2 - winner_text.get_width() // 2, 180)
        )

        final_score = font.render(
            f"Shaina {shaina_score} - {player2_score} Player 2",
            True,
            BLACK
        )

        screen.blit(
            final_score,
            (WIDTH // 2 - final_score.get_width() // 2, 260)
        )

        pygame.draw.rect(
            screen,
            RED,
            restart_button,
            border_radius=20
        )

        restart_text = font.render(
            "START AGAIN",
            True,
            WHITE
        )

        screen.blit(
            restart_text,
            (
                restart_button.x + restart_button.width // 2 - restart_text.get_width() // 2,
                restart_button.y + 20
            )
        )

    # GAME SCREEN
    else:

        # Controls
        keys = pygame.key.get_pressed()

        # Shaina
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED

        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED

        # Player 2
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED

        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

        # Move Ball
        ball.x += int(ball_speed_x)
        ball.y += int(ball_speed_y)

        # Bounce top/bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Paddle collision
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):

            ball_speed_x *= -1

            # Speed increase
            if ball_speed_x > 0:
                ball_speed_x += speed_boost
            else:
                ball_speed_x -= speed_boost

            if ball_speed_y > 0:
                ball_speed_y += speed_boost
            else:
                ball_speed_y -= speed_boost

        # Score system
        if ball.left <= 0:
            player2_score += 1
            reset_ball()

        if ball.right >= WIDTH:
            shaina_score += 1
            reset_ball()

        # Winner
        if shaina_score >= MAX_SCORE:
            winner = "SHAINA WINS!"
            game_over = True

        if player2_score >= MAX_SCORE:
            winner = "PLAYER 2 WINS!"
            game_over = True

        # Center line
        for i in range(0, HEIGHT, 30):

            pygame.draw.rect(
                screen,
                BLACK,
                (WIDTH // 2 - 2, i, 4, 20)
            )

        # Draw paddles
        pygame.draw.rect(screen, RED, left_paddle)
        pygame.draw.rect(screen, RED, right_paddle)

        # Neon glow ball
        for glow in range(30, 0, -5):

            pygame.draw.circle(
                screen,
                NEON,
                ball.center,
                BALL_SIZE // 2 + glow,
                1
            )

        pygame.draw.circle(
            screen,
            NEON,
            ball.center,
            BALL_SIZE // 2
        )

        # Scores
        shaina_text = title_font.render(
            str(shaina_score),
            True,
            BLACK
        )

        player2_text = title_font.render(
            str(player2_score),
            True,
            BLACK
        )

        screen.blit(shaina_text, (WIDTH // 4, 40))
        screen.blit(player2_text, (WIDTH * 3 // 4, 40))

        # Names
        shaina_name = font.render("Shaina", True, BLACK)
        player2_name = font.render("Player 2", True, BLACK)

        screen.blit(shaina_name, (WIDTH // 4 - 40, 100))
        screen.blit(player2_name, (WIDTH * 3 // 4 - 60, 100))

    pygame.display.update()

pygame.quit()