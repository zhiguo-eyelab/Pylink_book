#!/usr/bin/env python3
#
# Filename: demo.py
# Author: Zhiguo Wang
# Date: 2/4/2021
#
# Description:
# This short script shows how to request Pylink to use the
# EyeLinkCoreGraphcicPsychoPy library

import pylink
from psychopy import visual, core, event, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open a PsychoPy window
SCN_WIDTH, SCN_HEIGHT = (1280, 800)
win = visual.Window((SCN_WIDTH, SCN_HEIGHT),
                    fullscr=False,
                    units='pix')

# Pass display dimension (left, top, right, bottom) to the tracker
coords = "screen_pixel_coords = 0 0 {SCN_WIDTH - 1} {SCN_HEIGHT - 1}"
tk.sendCommand(coords)

# Create a custom graphics environment (genv) for calibration
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# Calibrate the tracker
# when a gray screen comes up, press Enter to show the camera image
# press C to calibrate, V to validate, O to exit the calibration routine
tk.doTrackerSetup()

# Close the connection to he tracker
tk.close()

# Quit PsychoPy
win.close()
core.quit()
