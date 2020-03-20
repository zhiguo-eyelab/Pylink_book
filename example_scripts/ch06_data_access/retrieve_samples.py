# Filename:retrieve_samples.py

import pylink

# connect to the tracker and open an EDF
tk = pylink.EyeLink('100.1.1.1')
tk.openDataFile('smp_test.edf')

# open a window to calibrate the tracker
pylink.openGraphics()
tk.doTrackerSetup()
pylink.closeGraphics()

tk.sendCommand('sample_rate 1000') # set sampling rate to 1000 Hz

# make sure gaze, HREF, and raw (PUPIL) data is available over the link
tk.sendCommand('link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT')

# start recording
error = tk.startRecording(1,1,1,1)
pylink.pumpDelay(100) # cache some samples for event parsing

# open a plain text file to write the sample data
text_file = open('sample_data.csv', 'w')

t_start = tk.trackerTime() # current tracker time
smp_time = -1
while True:
    # break after 10 seconds have elapsed
    if tk.trackerTime() - t_start > 3000:
        break
           
    # poll the latest samples
    dt = tk.getNewestSample()
    if dt is not None:
        if dt.isRightSample():
            gaze = dt.getRightEye().getGaze()
            href = dt.getRightEye().getHREF()
            raw  = dt.getRightEye().getRawPupil()
            pupil= dt.getRightEye().getPupilSize()
        elif dt.isLeftSample():
            gaze = dt.getLeftEye().getGaze()
            href = dt.getLeftEye().getHREF()
            raw  = dt.getLeftEye().getRawPupil()
            pupil= dt.getLeftEye().getPupilSize()

        timestamp = dt.getTime() 
        if timestamp > smp_time:
            smp = map(str,[dt.getTime(),gaze,href,raw,pupil])
            text_file.write('\t'.join(smp) + '\n')
            smp_time = timestamp
        
tk.stopRecording() # stop recording
tk.closeDataFile() # close EDF data file on the Host
text_file.close()
tk.close() #close the link to the tracker
