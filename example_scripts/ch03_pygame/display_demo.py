# Filename: display_demo.py

import pygame
from pygame.locals import *

pygame.init() # initialize Pygame modules

# open a window
win = pygame.display.set_mode((1024, 768), DOUBLEBUF|HWSURFACE|FULLSCREEN)

# create an empty list to save the monitor refresh intervals
intv = []

# flip the video buffer to make sure the first timestamp corresponds to a retrace
pygame.display.flip()

# get the timestamp of the 'previous' screen retrace
t_before_flip = pygame.time.get_ticks() 

# use a for-loop to flip the video buffer for 100 times 
for i in range(100):
    # constantly switching the window color between black and white
    if i%2 == 0:
        win.fill((255, 255, 255))
    else:
        win.fill((0,0,0))
    pygame.display.flip() # flip the video buffer

    # get the timestamp of the 'current' screen retrace
    t_after_flip = pygame.time.get_ticks()
    flip_intv = t_after_flip - t_before_flip # get the refresh interval
    intv.append(flip_intv) # save the current refresh interval to a list
    t_before_flip = t_after_flip # reset the timestamp of the 'previous' retrace

# print out the max, min and average refresh intervals
print('Max: {}, Min: {}, Mean: {}'.format(max(intv),
                                          min(intv),
                                          sum(intv)*1.0/len(intv)))
# quit pygame
pygame.quit()
