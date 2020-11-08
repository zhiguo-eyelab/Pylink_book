# Filename: interest_area.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# This script illustrates the IAREA messages
# that Data Viewer uses to reconstruct interest areas

import pylink

# Connect to the tracker
tk = pylink.EyeLink()

# Open an EDF on the Host; filename must not exceed 8 characters
tk.openDataFile('ias.edf')

# Run through five trials
for trial in range(1, 6):
    # Print out a message to show the current trial
    print("Trial #: %d" % trial)

    # Log a TRIALID message to mark trial start
    tk.sendMessage('TRIALID %d' % trial)

    # Start recording
    tk.startRecording(1, 1, 1, 1)

    # Pretending that we are doing something for 2-sec
    pylink.pumpDelay(2000)

    # Stop recording
    tk.stopRecording()
    
    # Send IAREA messages to store interest area definitions
    tk.sendMessage('!V IAREA ELLIPSE 1 0 0 100 100 head')
    tk.sendMessage('!V IAREA RECTANGLE 2 85 85 285 185 body')
    tk.sendMessage('!V IAREA FREEHAND 3 285,125 385,50 335,125 tail')

    # Log a TRIAL_RESULT message to mark trial ends
    tk.sendMessage('TRIAL_RESULT 0')

# Close the EDF file and download it from the Host PC
pylink.msecDelay(100)  # wait for 100 to catch session end events
tk.closeDataFile()
tk.receiveDataFile('ias.edf', 'interst_area_demo.edf')

# Close the link
tk.close()
