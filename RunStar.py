import pygame
import random

pygame.init()
pygame.font.init()  # Initialize the font module

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
button_rect = pygame.Rect(0, 0, 200, 70)  # Width and height
button_rect.center = (screen_width // 2, screen_height // 2 + 10)  # Position

# Button text properties
button_font = pygame.font.SysFont('Arial', 26)
button_text = button_font.render('START GAME', True, WHITE)
button_text_rect = button_text.get_rect(center=button_rect.center)

# Home text
welcome_font = pygame.font.SysFont('Impact', 30)
welcome_text = welcome_font.render('Welcome to RunStar', True, WHITE)
welcome_text_rect = welcome_text.get_rect(center=(screen_width // 2, 50))  # Position the text

# Player setup
player_size = (30, 30)  # Width and height of the player
player_pos = [screen_width // 2, screen_height - 100]
player_speed = 0.7  # Adjust as needed for appropriate speed
color_index = 0

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
screen_speed = 0.001  # Start with a smaller value
speed_increase = 0.00001  # Increment speed by a smaller amount

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
    global game_active, player_pos, screen_speed, speed_increase, obstacles
    game_active = False
    player_pos = [screen_width // 2, screen_height - 100]
    screen_speed = 0.001  # Reset to initial speed
    speed_increase = 0.00001  # Reset to initial speed increase
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
    keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

    # Move player based on key presses
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_pos[0] += player_speed

    # Keep the player within the screen bounds
    player_pos[0] = max(player_pos[0], 0)
    player_pos[0] = min(player_pos[0], screen_width - player_size[0])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse_pos) and not game_active:
                game_active = True  # This should start the game

    screen.fill(GREY)

    if game_active:
        # Update and draw obstacles
        for obstacle in obstacles:
            obstacle['pos'][1] += screen_speed
            # Reset obstacle to the top if it goes off the bottom
            if obstacle['pos'][1] > screen_height:
                obstacle['pos'] = [random.randint(0, screen_width - obstacle['size'][0]), -obstacle_height]
                obstacle['size'] = (random.randint(min_obstacle_width, max_obstacle_width), obstacle_height)
            # Draw the obstacle
            pygame.draw.rect(screen, RED, pygame.Rect(obstacle['pos'][0], obstacle['pos'][1], obstacle['size'][0], obstacle['size'][1]))

        # Draw the player as a triangle
        player_triangle = [
            (player_pos[0], player_pos[1] + player_size[1]),  # Bottom left
            (player_pos[0] + player_size[0] / 2, player_pos[1]),  # Top center
            (player_pos[0] + player_size[0], player_pos[1] + player_size[1])  # Bottom right
        ]
        pygame.draw.polygon(screen, Colorsforplayer[color_index], player_triangle)

        # Check for collisions
        if check_collision(player_pos, player_size, obstacles):
            reset_game()  # Reset the game if there is a collision

        # Increase the screen's speed to make the game harder over time
        screen_speed += speed_increase
    else:
        # Draw the start button
        current_button_color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, current_button_color, button_rect)
        screen.blit(button_text, button_text_rect)
        screen.blit(welcome_text, welcome_text_rect)

    pygame.display.flip()

pygame.quit()

