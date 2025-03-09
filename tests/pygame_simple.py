# This is a simple pygame script with a circle that expands and contracts

# Import libs
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 480, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Expanding Circle")

# Define Colors
BLUE = (30, 100, 200)
YELLOW = (255, 210, 0)

# Circle parameters
circle_radius = 20
max_radius = 100
expanding = True

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Expand or contract the circle
    if expanding:
        circle_radius += 1
        if circle_radius >= max_radius:
            expanding = False
    else:
        circle_radius -= 1
        if circle_radius <= 0:
            expanding = True

    # Clear the screen
    screen.fill(BLUE)

    # Draw the circle
    pygame.draw.circle(screen, YELLOW, (WIDTH // 2, HEIGHT // 2), circle_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()