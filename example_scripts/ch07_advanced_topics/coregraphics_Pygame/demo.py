# Filename: demo.py

# This short script shows how to request Pylink to use a custom CoreGraphics library

import pylink, pygame
from pygame.locals import *
from EyeLinkCoreGraphicsPyGame import EyeLinkCoreGraphicsPyGame

# initialize pygame and open a window
pygame.init()
w, h = (800, 600)
win = pygame.display.set_mode((w, h), FULLSCREEN| DOUBLEBUF, 32)

# connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# instantiate the custom calibration graphics
genv = EyeLinkCoreGraphicsPyGame(win,tk)

# configure the calibration target
genv.backgroundColor = (255,255,255)
genv.targetSize = 32

# open the calibration window
pylink.openGraphicsEx(genv)

#Gets the display surface and sends a mesage to EDF file;
tk.sendCommand("screen_pixel_coords =  0 0 %d %d" %(w-1, h-1))

# calibrate the tracker
tk.doTrackerSetup()

#Close the file and transfer it to Display PC
tk.close()
pygame.quit()

