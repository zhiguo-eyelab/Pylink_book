#!/usr/bin/env python3
#
# Filename: link_events.py
# Author: Zhiguo Wang
# Date: 2/6/2021
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
tk.sendCommand('link_event_filter = {}'.format(event_flgs))

# Open an SDL window for calibration
pylink.openGraphics()

# Set up the camera and calibrate the tracker
tk.doTrackerSetup()

# Put tracker in idle/offline mode before we start recording
tk.setOfflineMode()

# Start recording
error = tk.startRecording(1, 1, 1, 1)

# Cache some samples for event parsing
pylink.msecDelay(100)

# Get current tracker time
t_start = tk.trackerTime()
while True:
    # Break after 5 seconds have elapsed
    if tk.trackerTime() - t_start > 5000:
        break

    # Retrieve the oldest event in the buffer
    dt = tk.getNextData()
    if dt > 0:
        # Send a message to the tracker when an event is
        # received over the link; include the timestamp
        # in the message to examine the link delay
        ev = tk.getFloatData()
        if dt == pylink.STARTSACC:
            tk.sendMessage('STARTSACC {}'.format(ev.getTime()))
        if dt == pylink.ENDSACC:
            tk.sendMessage('ENDSACC {}'.format(ev.getTime()))
        if dt == pylink.STARTFIX:
            tk.sendMessage('STARTFIX {}'.format(ev.getTime()))
        if dt == pylink.ENDFIX:
            tk.sendMessage('ENDFIX {}'.format(ev.getTime()))

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
