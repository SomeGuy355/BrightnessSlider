import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from time import sleep

# Initialize pygame mixer
pygame.mixer.init()

# Load a sound file or create a silent sound
sound = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)  # Silent sound

# Play the sound
sound.play()

while True:
    sleep(100)
