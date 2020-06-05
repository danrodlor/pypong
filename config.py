import os
from pathlib import Path

# Paths
BASE_PATH = Path(__file__).parent
RESOURCES_BASE_PATH = os.path.join(BASE_PATH, 'resources')
SOUNDS_PATH = os.path.join(RESOURCES_BASE_PATH, 'sounds')
IMAGES_PATH = os.path.join(RESOURCES_BASE_PATH, 'images')
STORAGE_BASE_PATH = os.path.join(BASE_PATH, 'storage')

# Global variable to keep a paused game image as a string in RAM.
# Could this be done in a cleaner way? Creating/deleting the image in the fs every
# time is not the way to go as it is costly. The string buffer is a nice alternative.
PAUSED_GAME_IMG_STRING = None

# Game configuration variables
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 450
FPS = 60
BRICK_SIZE = 25
PLAYER_SPEED = 3
ENEMY_SPEED = 3
