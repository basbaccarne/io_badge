 # this is a simple script that does the following
    # it takes an animated gif
    # it loads the gif frames in pygame surfaces
    # # it displays the gif frames as an animation
 
 # libraries
from PIL import Image, ImageSequence
import pygame
import time
from pathlib import Path
import os
 
 # key variables
IMG_WIDTH = 480
IMG_HEIGHT = 480
FPS = 30

# PATHS
SCRIPT_DIR = Path(__file__).parent
IMG_DIR = SCRIPT_DIR.parent / 'img'

# function to load gif frames
def load_gif_frames(filename):
    image = Image.open(filename)
    frames = []
    for frame in ImageSequence.Iterator(image):
        frame = frame.convert("RGBA")
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()
        pygame_image = pygame.image.fromstring(data, size, mode)
        frames.append(pygame_image)
    return frames

# Quit the audio service, since we have no audo device
pygame.mixer.quit()

# Initialize Pygame
pygame.init()

# Set up the PyGame canvas (showing a 480 x 480 window)
screen = pygame.display.set_mode(
    (IMG_WIDTH, IMG_HEIGHT),
    pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME
)

# Preloading: Load the gif frames
print(f"Loading image from: {IMG_DIR / 'animation.gif'}")
frames = load_gif_frames(IMG_DIR / 'animation.gif')
frame_count = len(frames)
frame_index = 0
frame_delay = 1000 / FPS
print("GIF loaded!")

# Main loop
clock = pygame.time.Clock()
running = True
last_update = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update frame based on time
    if time.time() - last_update > frame_delay / 1000.0:
        frame_index = (frame_index + 1) % frame_count
        last_update = time.time()

    screen.fill((0, 0, 0))  # Clear screen
    screen.blit(frames[frame_index], (0, 0))  # Draw frame
    pygame.display.flip() # Render
    
    clock.tick(FPS) 

pygame.quit()