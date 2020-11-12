# Filename: event_demo.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# A short script showing how to handle Pygame events

import pygame
from pygame.locals import *

# Initialize Pygame and open a window
pygame.init()
scn = pygame.display.set_mode((640, 480))

# Constantly polling for new events in a while-loop
while True:
    ev_list = pygame.event.get()
    for ev in ev_list:
        # Mouse motion
        if ev.type == MOUSEMOTION:
            print(ev.pos)

        # Mouse button down
        if ev.type == MOUSEBUTTONDOWN:
            print(ev.button)

        # Key down
        if ev.type == KEYDOWN:
            print(ev.key)

        # Quit Pygame if the "close window" button is pressed
        if ev.type == QUIT:
            pygame.quit()
