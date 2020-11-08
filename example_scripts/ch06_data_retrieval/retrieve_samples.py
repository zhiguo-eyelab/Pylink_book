# Filename:retrieve_samples.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# A short script illustrating online retrieval of samples

import pylink

# Connect to the tracker and open an EDF
tk = pylink.EyeLink('100.1.1.1')
tk.openDataFile('smp_test.edf')

# Open a SDL window to calibrate the tracker
pylink.openGraphics()
tk.doTrackerSetup()
pylink.closeGraphics()

tk.sendCommand('sample_rate 1000')  # set sample rate to 1000 Hz

# Make gaze, HREF, and raw (PUPIL) data available over the link
sample_flag = 'LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT'
tk.sendCommand('link_sample_data = %s' % sample_flags)

# Start recording
error = tk.startRecording(1, 1, 1, 1)
pylink.msecDelay(100)  # cache some samples for event parsing

# Open a plain text file to store the retrieved sample data
text_file = open('sample_data.csv', 'w')

t_start = tk.trackerTime()  # current tracker time
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
        # Put gaze, HREF, raw, & pupil data to the plain text
        # file if the sample is new
        if timestamp > smp_time:
            smp = map(str, [timestamp, gaze, href, raw, pupil])
            text_file.write('\t'.join(smp) + '\n')
            smp_time = timestamp

tk.stopRecording()  # stop recording
tk.closeDataFile()  # close the EDF data file on the Host
text_file.close()  # close the plain text file
tk.close()  # close the link to the tracker
