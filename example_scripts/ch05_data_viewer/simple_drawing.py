#!/usr/bin/env python
#
# Filename: simple_drawing.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# This script illustrates the various drawing commands
# supported by Data Viewer

import pylink

# Connect to the tracker
tk = pylink.EyeLink()

# Open an EDF on the Host; filename must not exceed 8 characters
tk.openDataFile('drawing.edf')

# Assume the screen resolution is 1280 x 800 pixels
SCN_W, SCN_H = (1280, 800)

# Pass the screen coordinates to the tracker
coords = f'screen_pixel_coords = 0 0 {SCN_W - 1} {SCN_H - 1}'
tk.sendCommand(coords)

# Record a DISPLAY_COORDS message to let Data Viewer know the
# correct screen resolution to use when visualizing the data
tk.sendMessage(f'DISPLAY_COORDS 0 0 {SCN_W - 1} {SCN_H - 1}')

# Run through five trials
for trial in range(1, 6):
    # Print out a message to show the current trial
    print(f'Trial #: {trial}')

    # Log a TRIALID message to mark trial start
    tk.sendMessage(f'TRIALID {trial}')

    # Start recording
    tk.startRecording(1, 1, 1, 1)

    # Clear the screen to show a white background
    tk.sendMessage('!V CLEAR 255 255 255')
    # Draw a central fixation dot
    tk.sendMessage('!V FIXPOINT 0 0 0 0 0 0 512 384 25 0')
    # Draw the non-target
    tk.sendMessage('!V FIXPOINT 0 0 0 255 255 255 312 384 80 75')
    # Draw the target
    tk.sendMessage('!V FIXPOINT 255 0 0 255 0 0 712 384 80 0')

    # Pretending that we are doing something for 2-sec
    pylink.pumpDelay(2000)

    # Stop recording
    tk.stopRecording()

    # Log a TRIAL_RESULT message to mark trial ends
    tk.sendMessage('TRIAL_RESULT 0')

# Wait for 100 to catch session end events
pylink.msecDelay(100)

# Close the EDF file and download it from the Host PC
tk.closeDataFile()
tk.receiveDataFile('drawing.edf', 'drawing_demo.edf')

# Close the link
tk.close()
