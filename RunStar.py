import pygame

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
welcome_text = welcome_font.render('Welcome to RunStar', True, WHITE)  # White color text
welcome_text_rect = welcome_text.get_rect(center=(screen_width // 2, 50))  # Position the text

# Game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse_pos):
                print("Start clicked!")  
                

    # Button color change on hover
    if button_rect.collidepoint(mouse_pos):
        current_button_color = button_hover_color
    else:
        current_button_color = button_color

    # Fill the screen with grey color
    screen.fill(GREY)

    # Draw the button
    pygame.draw.rect(screen, current_button_color, button_rect)

    # Blit the button text onto the screen
    screen.blit(button_text, button_text_rect)

    # Blit the welcome text onto the screen
    screen.blit(welcome_text, welcome_text_rect)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()