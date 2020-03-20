# Filename: event_demo.py

import pygame
from pygame.locals import *

# initialize the modules and open a window
pygame.init()
scn = pygame.display.set_mode((640, 480))

while True:
    ev_list = pygame.event.get() 
    for ev in ev_list:
        # mouse motion
        if ev.type == MOUSEMOTION:
            print(ev.pos)
        if ev.type == MOUSEBUTTONDOWN:
            print(ev.button)
        # key down 
        if ev.type == KEYDOWN:
            print(ev.key)
        # close window button
        if ev.type == QUIT:
            pygame.quit()
