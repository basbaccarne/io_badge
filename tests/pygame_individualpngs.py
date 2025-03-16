 # this is a simple script that does the following
    # it loads a series of pngs in a folder img/frames
    # it displays the pngs as an animation
 
 # libraries
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

# function to load the pngs in the folder 'frames'
def load_png_frames(folder):
    frames = []
    for file in sorted(folder.glob('*.png')):
        frame = pygame.image.load(str(file))
        frames.append(frame)
    return frames

# set audio to dummy driver since we have no audo device
os.environ["SDL_AUDIODRIVER"] = "dummy"

# or even better quit the audio driver completely
pygame.mixer.quit()

# Initialize Pygame
pygame.init()

# Set up the PyGame canvas (showing a 480 x 480 window)
screen = pygame.display.set_mode(
    (IMG_WIDTH, IMG_HEIGHT),
    pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME
)

# Preloading: Load the gif frames
print(f"Loading png images from: {IMG_DIR / 'frames'}")
font = pygame.font.Font('freesansbold.ttf', 32)
text_surface = font.render('Some Text', False, (0, 0, 0))
text = font.render('Loading', True, (255, 255, 255))
textRect = text.get_rect()
textRect.center = (IMG_HEIGHT // 2, IMG_HEIGHT // 2)
screen.blit(text, textRect)
pygame.display.flip()

frames = load_png_frames(IMG_DIR / 'frames')
frame_count = len(frames)
frame_index = 0
frame_delay = 1000 / FPS
print("PNGs loaded!")

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