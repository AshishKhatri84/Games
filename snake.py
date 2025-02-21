import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (30, 30, 30)
RED = (200, 50, 80)
GREEN = (34, 177, 76)
BLUE = (135, 206, 250)

# Snake settings
SNAKE_BLOCK = 20
SNAKE_SPEED = 15

# Initialize display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("comicsansms", 40)
score_font = pygame.font.SysFont("comicsansms", 30)

def draw_gradient_background(color1, color2):
    """Creates a vertical gradient background."""
    for i in range(SCREEN_HEIGHT):
        color = [
            int(color1[j] + (color2[j] - color1[j]) * (i / SCREEN_HEIGHT)) for j in range(3)
        ]
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

def score_display(score):
    """Displays the score on the screen."""
    value = score_font.render(f"Your Score: {score}", True, YELLOW)
    screen.blit(value, (10, 10))

def draw_snake(snake_block, snake_list):
    """Draws the snake on the screen."""
    for x in snake_list:
        pygame.draw.rect(
            screen, BLACK, [x[0], x[1], snake_block, snake_block], border_radius=3
        )

def message(msg, color):
    """Displays a message on the screen."""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3))

def spawn_food():
    """Spawns food at a random position on the screen."""
    return (
        round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0,
        round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0,
    )

def game_loop():
    game_over = False
    game_close = False

    x1, y1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    foodx, foody = spawn_food()

    while not game_over:
        while game_close:
            draw_gradient_background((135, 206, 250), (70, 130, 180))
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            score_display(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -SNAKE_BLOCK, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = SNAKE_BLOCK, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change, y1_change = 0, -SNAKE_BLOCK
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change, y1_change = 0, SNAKE_BLOCK

        # Boundary collision
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        draw_gradient_background((135, 206, 250), (70, 130, 180))
        pygame.draw.rect(screen, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK], border_radius=5)

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check collision with self
        if snake_head in snake_list[:-1]:
            game_close = True

        draw_snake(SNAKE_BLOCK, snake_list)
        score_display(length_of_snake - 1)

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            foodx, foody = spawn_food()
            length_of_snake += 1

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

game_loop()
