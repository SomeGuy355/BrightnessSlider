import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from time import sleep

if getattr(sys, 'frozen', False):  # Running as an executable
    BASE_PATH = os.path.dirname(sys.executable)
else:  # Running as a script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Initialize pygame mixer
pygame.mixer.init()
pygame.display.init()

# Set the window icon (must be a 32x32 .ico file or a suitable .png)
icon = pygame.image.load(os.path.join(BASE_PATH,r"resources\brightness_icon.ico"))  # Replace with your icon file path
pygame.display.set_icon(icon)

# Set window title (optional, to make it more recognizable in the mixer)
pygame.display.set_caption("Your Application Title")

# Create a hidden window (sound mixer will still show it)
# screen = pygame.display.set_mode((1, 1))
screen = pygame.display.set_mode((1, 1), pygame.NOFRAME)  # Minimal, hidden window

# Load a sound file or create a silent sound
sound = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)  # Silent sound

# Play the sound
sound.play()

while True:
    sleep(100)
