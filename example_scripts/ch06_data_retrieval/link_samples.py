#!/usr/bin/env python3
#
# Filename: link_samples.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# A short script illustrating online retrieval of sample data

import pylink

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open an EDF data file on the Host PC
tk.openDataFile('smp_test.edf')

# Put the tracker in offline mode before we change tracking parameters
tk.setOfflineMode()

# Set sample rate to 1000 Hz
tk.sendCommand('sample_rate 1000')

# Make gaze, HREF, and raw (PUPIL) data available over the link
sample_flag = 'LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT'
tk.sendCommand('link_sample_data = {}'.format(sample_flag))

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

# Open a plain text file to store the retrieved sample data
text_file = open('sample_data.csv', 'w')

# Current tracker time
t_start = tk.trackerTime()  
smp_time = -1
while True:
    # Break after 5 seconds have elapsed
    if tk.trackerTime() - t_start > 5000:
        break

    # Poll the latest samples
    dt = tk.getNewestSample()
    if dt is not None:
        # Grab gaze, HREF, raw, & pupil size data
        if dt.isRightSample():
            gaze = dt.getRightEye().getGaze()
            href = dt.getRightEye().getHREF()
            raw = dt.getRightEye().getRawPupil()
            pupil = dt.getRightEye().getPupilSize()
        elif dt.isLeftSample():
            gaze = dt.getLeftEye().getGaze()
            href = dt.getLeftEye().getHREF()
            raw = dt.getLeftEye().getRawPupil()
            pupil = dt.getLeftEye().getPupilSize()

        timestamp = dt.getTime()
        
        # Save gaze, HREF, raw, & pupil data to the plain text
        # file, if the sample is new
        if timestamp > smp_time:
            smp = map(str, [timestamp, gaze, href, raw, pupil])
            text_file.write('\t'.join(smp) + '\n')
            smp_time = timestamp

# Stop recording
tk.stopRecording()

# Close the plain text file
text_file.close()  

# Close the EDF data file on the Host
tk.closeDataFile()

# Download the EDF data file from Host
tk.receiveDataFile('smp_test.edf', 'smp_test.edf')

# Close the link to the tracker
tk.close()

# Close the window
pylink.closeGraphics()
