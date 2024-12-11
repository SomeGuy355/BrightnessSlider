import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# import pygame
from pygame import mixer
from time import sleep

if __name__ == '__main__':
    # Initialize pygame mixer
    # pygame.mixer.init()
    mixer.init()

    # Load a sound file or create a silent sound
    # sound = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)  # One second?, silent sound
    sound = mixer.Sound(buffer=b'\x00\x00' * 1000)  # One second?, silent sound

    # Play the sound
    sound.play()

    while True:
        sleep(10000) # not sure how long this needs/can be? nor if this script is particularly CPU intensive? or like overhead/ram kinda usage
