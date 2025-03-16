
# key variables
IMG_WIDTH = 480
IMG_HEIGHT = 480
FPS = 30
N_COL = 10
N_ROW = 44
TOTAL_FRAMES = 438

# Libraries
import pygame
from pathlib import Path
import os

# PATHS
SCRIPT_DIR = Path(__file__).parent
IMG_DIR = SCRIPT_DIR.parent / 'img'

# set audio to dummy driver since we have no audo device
os.environ["SDL_AUDIODRIVER"] = "dummy"

# or even better quit the audio driver completely
pygame.mixer.quit()

# Initialize Pygame
pygame.init()

# Load the spritesheet
print(f"Loading image from: {IMG_DIR / 'spritesheet2.png'}")
spritesheet = pygame.image.load(str(IMG_DIR / 'spritesheet2.png'))
print("Spritesheet loaded!")

# Define the dimensions of each frame in the spritesheet
frame_width = IMG_WIDTH
frame_height = IMG_HEIGHT

# Function to extract a frame from the spritesheet
def get_frame(row, col):
    frame = spritesheet.subsurface(pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height))
    return frame

# Create a list of frames for animation
frames = []
for row in range(N_ROW):
    for col in range(N_COL):
        if row == N_ROW - 1 and col >= TOTAL_FRAMES % N_COL:
            break  # Skip invalid frames in the last row
        frame = spritesheet.subsurface(pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height))
        frames.append(frame)

# Set up the PyGame canvas (showing a 480 x 480 window)
screen = pygame.display.set_mode(
    (IMG_WIDTH, IMG_HEIGHT),
    pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME
)


# Initialize key PyGame parameters
clock = pygame.time.Clock()
current_frame = 0
running = True
print("Pygame running ...")
# Run the PyGame
while running:
    # Handle events and quit if necessary
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Load the frame (on position 0,0)
    screen.blit(frames[current_frame], (0, 0))

    # increment the framecount
    current_frame = (current_frame + 1) % len(frames)

    # Update the screen
    pygame.display.update()

    # Control the framerate
    clock.tick(FPS)

pygame.quit()