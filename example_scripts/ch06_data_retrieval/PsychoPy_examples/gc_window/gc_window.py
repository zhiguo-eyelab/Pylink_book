#!/usr/bin/env python3
#
# Filename: gc_window.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# A gaze-contingent window task implemented in PsychoPy

import pylink
from psychopy import visual, core, event, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open an EDF data file
tk.openDataFile('psychopy.edf')

# Put the tracker in offline mode before we change tracking parameters
tk.setOfflineMode()

# Make all types of sample data available over the link
sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT'
tk.sendCommand(f'link_sample_data  = {sample_flags}')

# Screen resolution
SCN_W, SCN_H = (1280, 800)

# Open a PsyhocPy window with the "allowStencil" option
win = visual.Window((SCN_W, SCN_H), fullscr=False,
                    units='pix', allowStencil=True)

# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
coords = f"screen_pixel_coords = 0 0 {SCN_W - 1} {SCN_H - 1}"
tk.sendCommand(coords)

# Request Pylink to use the custom EyeLinkCoreGraphicsPsychoPy library
# to draw calibration graphics (target, camera image, etc.)
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# Calibrate the tracker
calib_msg = visual.TextStim(win, text='Press ENTER to calibrate')
calib_msg.draw()
win.flip()
tk.doTrackerSetup()

# Set up a aperture and use it as a gaze-contingent window
gaze_window = visual.Aperture(win, shape='square', size=200)
gaze_window.enabled = True

# Load a background image to fill up the screen
img = visual.ImageStim(win, image='woods.jpg', size=(SCN_W, SCN_H))

# Put tracker in Offline mode before we start recording
tk.setOfflineMode()

# Start recording
tk.startRecording(1, 1, 1, 1)

# Cache some samples
pylink.msecDelay(100)

# show the image indefinitely until a key is pressed
gaze_pos = (-32768, -32768)
while not event.getKeys():
    # Check for new samples
    dt = tk.getNewestSample()
    if dt is not None:
        if dt.isRightSample():
            gaze_x, gaze_y = dt.getRightEye().getGaze()
        elif dt.isLeftSample():
            gaze_x, gaze_y = dt.getLeftEye().getGaze()

        # Draw the background image
        img.draw()
        
        # Update the window with the current gaze position
        gaze_window.pos = (gaze_x - SCN_W/2.0, SCN_H/2.0 - gaze_y)
        win.flip()

# Stop recording
tk.stopRecording()

# Close the EDF data file on the Host
tk.closeDataFile()

# Download the EDF data file from Host
tk.receiveDataFile('psychopy.edf', 'psychopy.edf')

# Close the link to the tracker
tk.close()

# Close the graphics
win.close()
core.quit()

