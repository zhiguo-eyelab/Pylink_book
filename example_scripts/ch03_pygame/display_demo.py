#!/usr/bin/env python3
#
# Filename: display_demo.py
# Author: Zhiguo Wang
# Date: 2/11/2021
#
# Description:
# Open an widnow to assess monitor refresh consistency

import pygame
from pygame.locals import *

# Initialize Pygame & its modules
pygame.init()

# Get the native resolution supported by the monitor
scn_res = pygame.display.list_modes()[0]

# Open a window
win = pygame.display.set_mode(scn_res, DOUBLEBUF | HWSURFACE | FULLSCREEN)

# An empty list to store the monitor refresh intervals
intv = []

# Flip the video buffer, then grab the timestamp of the first retrace
pygame.display.flip()

# Get the timestamp of the 'previous' screen retrace
t_before_flip = pygame.time.get_ticks()

# Use a for-loop to flip the video buffer for 200 times
for i in range(200):
    # Switching the window color between black and white
    if i % 2 == 0:
        win.fill((255, 255, 255))
    else:
        win.fill((0, 0, 0))
    # Flip the video buffer to show the screen
    pygame.display.flip()

    # Get the timestamp of the 'current' screen retrace
    t_after_flip = pygame.time.get_ticks()
    # Get the refresh interval
    flip_intv = t_after_flip - t_before_flip
    # Store the refresh interval to "intv"
    intv.append(flip_intv)
    # Reset the timestamp of the 'previous' retrace
    t_before_flip = t_after_flip

# Print out the max, min and average refresh intervals
intv_max = max(intv)
intv_min = min(intv)
intv_avg = sum(intv)*1.0/len(intv)
print('Max: {}, Min: {}, Mean: {}'.format(intv_max, intv_min, intv_avg))

# Quit Pygame
pygame.quit()
