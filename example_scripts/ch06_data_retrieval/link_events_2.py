#!/usr/bin/env python3
#
# Filename: link_events_2.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# A short script illustrating online retrieval of eye events


import pylink

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open an EDF data file on the Host PC
tk.openDataFile('ev_test2.edf')

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
el_tracker.setOfflineMode()

# Start recording
error = tk.startRecording(1, 1, 1, 1)

# Cache some samples for event parsing
pylink.msecDelay(100)

# Current tracker time
t_start = tk.trackerTime()
while True:
    # Break after 5 seconds have elapsed
    if tk.trackerTime() - t_start > 5000:
        break

    # Retrieve the oldest event in the buffer
    dt = tk.getNextData()
    if dt > 0:
        ev = tk.getFloatData()
        if dt == pylink.ENDSACC:
            print('ENDSACC Event: \n',
                  'Amplitude', ev.getAmplitude(), '\n',
                  'Angle', ev.getAngle(), '\n',
                  'AverageVelocity', ev.getAverageVelocity(), '\n',
                  'PeakVelocity', ev.getPeakVelocity(), '\n',
                  'StartTime', ev.getStartTime(), '\n',
                  'StartGaze', ev.getStartGaze(), '\n',
                  'StartHREF', ev.getStartHREF(), '\n',
                  'StartPPD', ev.getStartPPD(), '\n',
                  'StartVelocity', ev.getStartVelocity(), '\n',
                  'EndTime', ev.getEndTime(), '\n',
                  'EndGaze', ev.getEndGaze(), '\n',
                  'EndHREF', ev.getEndHREF(), '\n',
                  'StartPPD', ev.getStartPPD(), '\n',
                  'EndVelocity', ev.getEndVelocity(), '\n',
                  'Eye', ev.getEye(), '\n',
                  'Time', ev.getTime(), '\n',
                  'Type', ev.getType(), '\n')

# Stop recording
tk.stopRecording()

# Close the EDF data file on the Host
tk.closeDataFile()

# Download the EDF data file from Host
tk.receiveDataFile('ev_test2.edf', 'ev_test2.edf')

# Close the link to the tracker
tk.close()

# Close the window
pylink.closeGraphics()
