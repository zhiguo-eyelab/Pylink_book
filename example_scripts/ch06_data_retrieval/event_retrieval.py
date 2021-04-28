#!/usr/bin/env python3
#
# Filename: event_retrieval.py
# Author: Zhiguo Wang
# Date: 4/26/2021
#
# Description:
# A short script illustrating online retrieval of eye events

import pylink

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open an EDF data file on the Host PC
tk.openDataFile('ev_test.edf')

# Put the tracker in offline mode before we change tracking parameters
tk.setOfflineMode()

# Set sample rate to 1000 Hz
tk.sendCommand('sample_rate 1000')

# Make all types of event data are available over the link
event_flgs = 'LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT'
tk.sendCommand(f'link_event_filter = {event_flgs}')

# Open an SDL window for calibration
pylink.openGraphics()

# Set up the camera and calibrate the tracker
tk.doTrackerSetup()

# Put tracker in idle/offline mode before we start recording
tk.setOfflineMode()

# Start recording
tk.startRecording(1, 1, 1, 1)

# Wait for the block start event to arrive, give a warning
# if no event or sample is available
block_start = tk.waitForBlockStart(100, 1, 1)
if block_start == 0:
    print("ERROR: No link data received!")

# Check eye availability; 0-left, 1-right, 2-binocular
# read data from the right eye if tracking in binocular mode
eye_to_read = tk.eyeAvailable()
if eye_to_read == 2:
    eye_to_read = 1

# Get the current tracker time
t_start = tk.trackerTime()
while True:
    # Break after 5 seconds have elapsed
    if tk.trackerTime() - t_start > 5000:
        break

    # Retrieve the oldest event in the buffer
    dt = tk.getNextData()
    if dt > 0:
        ev = tk.getFloatData()
        # Look for right eye events only; 0-left, 1-right
        if ev.getEye() == eye_to_read： 
            # Send a message to the tracker when an event is
            # received over the link; include the timestamp
            # in the message to examine the link delay
            if dt == pylink.STARTSACC:
                tk.sendMessage(f'STARTSACC {ev.getTime()}')
            if dt == pylink.ENDSACC:
                tk.sendMessage(f'ENDSACC {ev.getTime()}')
            if dt == pylink.STARTFIX:
                tk.sendMessage(f'STARTFIX {ev.getTime()}')
            if dt == pylink.ENDFIX:
                tk.sendMessage(f'ENDFIX {ev.getTime()}')

# Stop recording
tk.stopRecording()

# Close the EDF data file on the Host
tk.closeDataFile()

# Download the EDF data file from Host
tk.receiveDataFile('ev_test.edf', 'ev_test.edf')

# Close the link to the tracker
tk.close()

# Close the window
pylink.closeGraphics()
