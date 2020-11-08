# Filename: simple_drawing.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# This script illustrates the various drawing commands
# supported by Data Viewer

import pylink

# Connect to the tracker
tk = pylink.EyeLink()

# Open an EDF on the Host; filename must not exceed 8 characters
tk.openDataFile('drawing.edf')

# Run through five trials
for trial in range(1, 6):
    # Print out a message to show the current trial
    print("Trial #: %d" % trial)

    # Log a TRIALID message to mark trial start
    tk.sendMessage('TRIALID %d' % trial)

    # Start recording
    tk.startRecording(1, 1, 1, 1)

    # Draw a central fixation flanked by two possible targets
    # Clear the screen to show white background
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

# Close the EDF file and download it from the Host PC
pylink.msecDelay(100)  # wait for 100 to catch session end events
tk.closeDataFile()
tk.receiveDataFile('drawing.edf', 'drawing_demo.edf')

# Close the link
tk.close()
