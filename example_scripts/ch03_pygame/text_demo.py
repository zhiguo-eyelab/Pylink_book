#!/usr/bin/env python3
#
# Filename: text_demo.py
# Author: Zhiguo Wang
# Date: 2/7/2021
#
# Description:
# Text rendering example in Pygame

import pygame, sys

# Initialize Pygame
pygame.init()

# Open a window
win = pygame.display.set_mode((300,200))

# Create a font object and enable 'underline'
fnt = pygame.font.SysFont('arial', 32, bold=True, italic=True)
fnt.set_underline(True)

# Using the size() method to estimates the width and height of
# the rendered text surface
demo_text = 'Hello, World!'
w, h = fnt.size(demo_text)

# Render the text to get a text surface
win.fill((0, 0, 0))
text_surf = fnt.render(demo_text, True, (255,0,0))

# Show(blit) the text surface at the window center
win.blit(text_surf, (150-w/2,100-h/2))
pygame.display.flip()

# Show the text until a key is pressed
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.KEYUP: 
            pygame.quit()
            sys.exit()
