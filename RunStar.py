import pygame
import random
import os

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen setup
screen_width, screen_height = 680, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Run Star")

# Define colors
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (150, 0, 255)
Colorsforplayer = [BLUE, GREEN, RED, PURPLE]

# Button properties
button_color = (0, 200, 0)
button_hover_color = (0, 255, 0)
button_rect = pygame.Rect(0, 0, 200, 70)
button_rect.center = (screen_width // 2, screen_height // 2 + 10)

# Button text properties
button_font = pygame.font.SysFont('Arial', 26)
button_text = button_font.render('START GAME', True, WHITE)
button_text_rect = button_text.get_rect(center=button_rect.center)

# Home text
welcome_font = pygame.font.SysFont('Impact', 30)
welcome_text = welcome_font.render('Welcome to RunStar', True, WHITE)
welcome_text_rect = welcome_text.get_rect(center=(screen_width // 2, 50))

# Player setup
player_size = (30, 30)
player_pos = [screen_width // 2, screen_height - 100]
player_speed = 0.7
color_index = 0

# Score system
score = 0
highscore = 0

# File operations for high score
def save_highscore(highscore):
    with open('highscore.txt', 'w') as file:
        file.write(str(int(highscore)))

def load_highscore():
    if os.path.exists('highscore.txt'):
        with open('highscore.txt', 'r') as file:
            try:
                return int(file.read())
            except ValueError:
            
                return 0

# Load the high score at the start
highscore = load_highscore()

def update_highscore(new_score):
    global highscore
    rounded_score = int(round(new_score))  # Convert to int before comparing
    if rounded_score > highscore:
        highscore = rounded_score
        save_highscore(highscore)

# Obstacle setup
min_obstacle_width = 50
max_obstacle_width = 150
obstacle_height = 20
num_obstacles = 5
obstacles = [
    {
        'pos': [random.randint(0, screen_width - max_obstacle_width), random.randint(-screen_height, 0)],
        'size': (random.randint(min_obstacle_width, max_obstacle_width), obstacle_height),
    } for _ in range(num_obstacles)
]

# Game state
game_active = False

# Screen speed
screen_speed = 0.01
speed_increase = 0.00001

# Function to check collision
def check_collision(player_pos, player_size, obstacles):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle['pos'][0], obstacle['pos'][1], obstacle['size'][0], obstacle['size'][1])
        if player_rect.colliderect(obstacle_rect):
            return True
    return False

# Function to reset the game
def reset_game():
    global game_active, player_pos, screen_speed, speed_increase, obstacles, score
    game_active = False
    player_pos = [screen_width // 2, screen_height - 100]
    screen_speed = 0.01
    speed_increase = 0.00001
    score = 0
    obstacles = [
        {
            'pos': [random.randint(0, screen_width - max_obstacle_width), random.randint(-screen_height, 0)],
            'size': (random.randint(min_obstacle_width, max_obstacle_width), obstacle_height),
        } for _ in range(num_obstacles)
    ]

# Game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_pos[0] += player_speed

    player_pos[0] = max(player_pos[0], 0)
    player_pos[0] = min(player_pos[0], screen_width - player_size[0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse_pos) and not game_active:
                game_active = True

    screen.fill(GREY)

    # Display the high score on the home screen
    high_score_display = button_font.render(f'High Score: {highscore}', True, WHITE)
    screen.blit(high_score_display, (screen_width - high_score_display.get_width() - 10, 10))

    if game_active:
        for obstacle in obstacles:
            obstacle['pos'][1] += screen_speed
            if obstacle['pos'][1] > screen_height:
                obstacle['pos'] = [random.randint(0, screen_width - obstacle['size'][0]), -obstacle_height]
                obstacle['size'] = (random.randint(min_obstacle_width, max_obstacle_width), obstacle_height)
            pygame.draw.rect(screen, RED, pygame.Rect(obstacle['pos'][0], obstacle['pos'][1], obstacle['size'][0], obstacle['size'][1]))

        score += 0.01
        display_score = int(round(score))
        score_text = button_font.render(f'Score: {display_score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        player_triangle = [
            (player_pos[0], player_pos[1] + player_size[1]),
            (player_pos[0] + player_size[0] / 2, player_pos[1]),
            (player_pos[0] + player_size[0], player_pos[1] + player_size[1])
        ]
        pygame.draw.polygon(screen, Colorsforplayer[color_index], player_triangle)

        if check_collision(player_pos, player_size, obstacles):
            update_highscore(score)
            reset_game()

        screen_speed += speed_increase

    else:
        current_button_color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, current_button_color, button_rect)
        screen.blit(button_text, button_text_rect)
        screen.blit(welcome_text, welcome_text_rect)

    pygame.display.flip()

pygame.quit()

