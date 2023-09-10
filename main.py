import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 500
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
GAME_SPEED = 100

# Colors
FOOD_COLOR = (240, 0, 0)
SCORE_FONT_COLOR = (255, 0, 120)
WHITE = (255,255,255)
SNAKE_COLOR = "green"
BACKGROUND_COLOR = (185, 243, 228)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
icon = pygame.image.load("snake (1).png")
pygame.display.set_icon(icon)

font2 = pygame.font.Font("Lazy Monday.otf", 60)

def main():
    game_over = False
    # Initialize the Snake
    snake = [(GRID_WIDTH // 2 , GRID_HEIGHT // 2 )]  #[(15, 10)]
    snake_direction = (1, 0)

    # Initialize the food
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    # Initialize the score
    score = 0
    font = pygame.font.Font("Lazy Monday.otf", 35)

    #Music Section
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play(-1)

    # Displaying High Score
    with open("highScore.txt") as file:
        high_score = file.read()

    def starting_screen():
        enter_text = pygame.font.Font("Lazy Monday.otf", 44)
        back_img = pygame.image.load("2589668_15587.jpg")
        resized_back_img = pygame.transform.scale(back_img, (800, 500))
        running = True

        while running:
            screen.blit(resized_back_img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_SPACE:    
                        running = False

            welcome_text = font2.render("Welcome to Snake Game!", True, WHITE)
            play_text = enter_text.render("Press SPACE to Play ", True, WHITE)
            screen.blit(welcome_text, (190, 120))
            screen.blit(play_text, (300, 230))

            pygame.display.update()

    starting_screen()

    def show_game_over_screen():

        screen.fill((255, 109, 96))
        game_over_text = font2.render("Game Over!", True, WHITE)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        exit_game_text = font.render("Press Q to exit game", True, WHITE)

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_q]:
            sys.exit()

        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        game_exit_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(final_score_text, final_score_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(exit_game_text, game_exit_rect)
        pygame.display.update()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:     
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)
        if not game_over:
            # Move the snake
            new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

            # Check for collisions
            if new_head == food:
                sound = pygame.mixer.Sound("Beep Short .mp3")
                sound.play(0)
                snake.insert(0, new_head)
                score += 1
                if score > int(high_score):
                    high_score = score
                food = (random.randint(0, GRID_WIDTH - 1), random.randint(4, GRID_HEIGHT - 1))
            else:
                if new_head in snake or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
                    game_over = True

                snake.insert(0, new_head)
                if len(snake) > score + 1:
                    snake.pop()

            # Clear the screen
            game_bg_img = pygame.image.load("back.jpg")
            resized_img = pygame.transform.scale(game_bg_img, (800, 500))
            screen.blit(resized_img, (0, 0))

            # Draw the snake
            for segment in snake:
                pygame.draw.rect(screen, SNAKE_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Draw the food
            pygame.draw.rect(screen, FOOD_COLOR, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE-5, GRID_SIZE-5))

            # Render the score text
            score_text = font.render(f"Score : {score}   HighScore: {high_score}", True, SCORE_FONT_COLOR)
            screen.blit(score_text, (10, 0))

            # Update the display
            pygame.display.update()
            
            # Control game speed
            pygame.time.delay(GAME_SPEED)

        else: 
            show_game_over_screen()
            with open("highScore.txt", "w") as f:
                f.write(str(high_score))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()


if __name__ == "__main__":
    main()

pygame.quit()
