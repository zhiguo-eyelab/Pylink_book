# Filename: retrieve_events.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# A short script illustrating online retrieval of eye events

import pylink

# Connect to the tracker and open an EDF
tk = pylink.EyeLink('100.1.1.1')
tk.openDataFile('ev_test.edf')

tk.sendCommand('sample_rate 1000')  # set sample rate to 1000 Hz

# Make all types of event data are available over the link
event_flgs = 'LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT'
tk.sendCommand('link_event_filter = %s' % event_flgs)

# Open an SDL window to calibrate the tracker
pylink.openGraphics()
tk.doTrackerSetup()
pylink.closeGraphics()

# Start recording
error = tk.startRecording(1, 1, 1, 1)
pylink.msecDelay(100)  # cache some samples for event parsing

t_start = tk.trackerTime()  # current tracker time
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
            tk.sendMessage('STARTSACC %d' % ev.getTime())
        if dt == pylink.ENDSACC:
            tk.sendMessage('ENDSACC %d' % ev.getTime())
        if dt == pylink.STARTFIX:
            tk.sendMessage('STARTFIX %d' % ev.getTime())
        if dt == pylink.ENDFIX:
            tk.sendMessage('ENDFIX %d' % ev.getTime())

tk.stopRecording()  # stop recording
tk.closeDataFile()  # close the EDF data file on the Host
# Download the EDF data file from Host
tk.receiveDataFile('ev_test.edf', 'ev_test.edf')
tk.close()  # close the link to the tracker
