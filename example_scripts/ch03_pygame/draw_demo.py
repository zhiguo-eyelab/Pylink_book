# Filename: draw_demo.py

import pygame, sys
from pygame.locals import *

pygame.init() # initialize pygame

# open a window
scn = pygame.display.set_mode((640, 480))

# create an empty list to store clicked screen positions
points = []

while True:
    # poll all pygame events
    for ev in pygame.event.get():
        # quit pygame and Python if the "close" button is clicked
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()
        
        # append the current mouse position to the list when 
        if ev.type == MOUSEBUTTONDOWN:
            points.append(ev.pos)

    # clear the screen
    scn.fill((255,255,255))
    
    # draw a polygon after three mouse clicks    
    if len(points) >= 3:
        pygame.draw.polygon(scn, (0,255,0), points)

    # show the screen locations that has been clicked
    for point in points:
        pygame.draw.circle(scn, (0,0,255), point, 10)

    # flip the video buffer to show the drawings
    pygame.display.flip()
