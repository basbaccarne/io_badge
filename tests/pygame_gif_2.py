# This script plays a spritesheet as an animation.
# Added: custom animation
'''
Core parameters:
* img size: 480x480
* img frames: 438
* framerate: 30 FPS
* column count: 10
* row count: 44
'''

# Libraries
import pygame

# Initialize Pygame
pygame.init()

# Load the spritesheet
spritesheet = pygame.image.load('img/spritesheet2.png')

# Define the dimensions of each frame in the spritesheet
frame_width = 480
frame_height = 480

# Function to extract a frame from the spritesheet
def get_frame(row, col):
    frame = spritesheet.subsurface(pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height))
    return frame

# Create a list of frames for animation
frames = []

# Set nr of columns & rows
num_cols = 10 
num_rows = 44 
total_frames = 438  # Total valid frames

# Calculate how many frames there are in the last row
last_row_frames = total_frames % num_cols  # Frames in the last row (e.g., 116 % 10 = 6)

# Go through the sheet and fill the list of frames
for row in range(num_rows):
    for col in range(num_cols):
        # Skip invalid frames in the last row
        if row == num_rows - 1 and col >= last_row_frames:
            continue
        frames.append(get_frame(row, col))

# Set up the PyGame canvas (showing a 480 x 480 window)
screen = pygame.display.set_mode((480, 480))

# Initialize key PyGame parameters
clock = pygame.time.Clock()
current_frame = 0
running = True

# Run the PyGame
while running:
    
    # reset background between frames (especially important for frames with transparent backgrounds)
    screen.fill((0, 0, 0))

    # Load the frame (on position 0,0)
    screen.blit(frames[current_frame], (0, 0))

    # increment the framecount
    current_frame = (current_frame + 1) % len(frames)

    # Update the screen
    pygame.display.flip()

    # Control the framerate
    clock.tick(30)

    # Exit function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()