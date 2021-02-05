# Filename: demo.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# This script shows how to request Pylink to use a custom calibration
# graphics library -- EyeLinkCoreGraphcicPsychoPy

import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open a PsychoPy window
SCN_WIDTH, SCN_HEIGHT = (1024, 768)

# Be sure to explicitly set monitor parameters
mon = monitors.Monitor('myMac15', width=53.0, distance=70.0)
win = visual.Window((SCN_WIDTH, SCN_HEIGHT), fullscr=False,
                    monitor=mon, units='pix')

# instantiate a custom CoreGraphics environment in PsychoPy
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# Set up the camera and calibrate the tracker
tk.doTrackerSetup()

# Close the connection and close the PsychoPy window
tk.close()
win.close()
core.quit()
