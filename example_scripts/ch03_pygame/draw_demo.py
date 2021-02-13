#!/usr/bin/env python3
#
# Filename: draw_demo.py
# Author: Zhiguo Wang
# Date: 2/7/2021
#
# Description:
# A script illustrating the drawing functions in Pygame

import pygame
import sys
from pygame.locals import *

# Initialize pygame and open a window
pygame.init()

# Open a window
scn = pygame.display.set_mode((640, 480))

# An empty list to store clicked screen positions
points = []

while True:
    # Poll Pygame events
    for ev in pygame.event.get():
        # Quit Pygame and Python if the "close window"
        # button is clicked
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()

        # Append the current mouse position to the list when
        # a mouse button down event is detected
        if ev.type == MOUSEBUTTONDOWN:
            points.append(ev.pos)

    # Clear the screen
    scn.fill((255, 255, 255))

    # Draw a polygon after three mouse clicks
    if len(points) >= 3:
        pygame.draw.polygon(scn, (0, 255, 0), points)

    # Highlight the screen locations that has been clicked
    for point in points:
        pygame.draw.circle(scn, (0, 0, 255), point, 10)

    # Flip the video buffer to show the drawings
    pygame.display.flip()
