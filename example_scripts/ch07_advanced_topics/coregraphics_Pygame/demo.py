# Filename: demo.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# This short script shows how to request Pylink to use
# a custom CoreGraphics library

import pylink
import pygame
from EyeLinkCoreGraphicsPyGame import EyeLinkCoreGraphicsPyGame

# Initialize pygame and open a window
pygame.init()
win = pygame.display.set_mode((800, 600))

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Instantiate the custom calibration graphics
genv = EyeLinkCoreGraphicsPyGame(tk, win)

# Configure the calibration target
genv.bgColor = (128, 128, 128)
genv.fgColor = (0, 0, 0)
genv.targetSize = 32

# Open the calibration window
pylink.openGraphicsEx(genv)

# Setup the camera and calibrate the tracker
tk.doTrackerSetup()

# Close the link and quit Pygame
tk.close()
pygame.quit()
