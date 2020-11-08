# Filename: demo.py

# This short script shows how to request Pylink to use
# a custom CoreGraphics library

import pylink, pygame
from EyeLinkCoreGraphicsPyGame import EyeLinkCoreGraphicsPyGame

# initialize pygame and open a window
pygame.init()
win = pygame.display.set_mode((800, 600))

# connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# instantiate the custom calibration graphics
genv = EyeLinkCoreGraphicsPyGame(tk,win)

# configure the calibration target
genv.bgColor = (128,128,128)
genv.fgColor = (0,0,0)
genv.targetSize = 32

# open the calibration window
pylink.openGraphicsEx(genv)

# setup the camera and calibrate the tracker
tk.doTrackerSetup()

# Close the link and quit pygame
tk.close()
pygame.quit()

