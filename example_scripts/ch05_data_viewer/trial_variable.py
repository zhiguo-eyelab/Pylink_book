#!/usr/bin/env python3
#
# Filename: trial_variable.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# This script illustrates the TRIAL_VAR messages
# that Data Viewer uses to parse variables

import pylink

# Connect to the tracker
tk = pylink.EyeLink()

# Open an EDF on the Host; filename must not exceed 8 characters
tk.openDataFile('vars.edf')

# Run through five trials
for trial in range(1, 6):
    # Print out a message to show the current trial
    print("Trial #: {}".format(trial))

    # Log a TRIALID message to mark trial start
    tk.sendMessage('TRIALID {}'.format(trial))

    # Start recording
    tk.startRecording(1, 1, 1, 1)

    # Pretending that we are doing something for 2-sec
    pylink.pumpDelay(2000)

    # Stop recording
    tk.stopRecording()

    # Send TRIAL_VAR messages to store variables in the EDF
    tk.sendMessage('!V TRIAL_VAR condition step')
    tk.sendMessage('!V TRIAL_VAR gap_duration 200')
    tk.sendMessage('!V TRIAL_VAR direction Right')

    # Log a TRIAL_RESULT message to mark trial ends
    tk.sendMessage('TRIAL_RESULT 0')

# Wait for 100 to catch session end events
pylink.msecDelay(100)  

# Close the EDF file and download it from the Host PC
tk.closeDataFile()
tk.receiveDataFile('vars.edf', 'trial_variable_demo.edf')

# Close the link
tk.close()
