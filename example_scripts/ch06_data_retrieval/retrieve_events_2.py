# Filename: retrieve_events_2.py

import pylink

# connect to the tracker and open an EDF
tk = pylink.EyeLink('100.1.1.1')
tk.openDataFile('ev_test.edf')

tk.sendCommand('sample_rate 1000') # set sampling rate to 1000 Hz

# make sure all types of event data are available over the link
tk.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")

# open a window to calibrate the tracker
pylink.openGraphics()
tk.doTrackerSetup()
pylink.closeGraphics()

# start recording
error = tk.startRecording(1,1,1,1)
pylink.pumpDelay(100) # cache some samples for event parsing

t_start = tk.trackerTime() # current tracker time
while True:
    # break after 5 seconds have elapsed
    if tk.trackerTime() - t_start > 5000:
        break
   
    dt = tk.getNextData()
    if dt > 0:
        ev = tk.getFloatData()
        if dt == pylink.ENDSACC: 
            print('ENDSACC Event: \n',
                  'Amplitude',      ev.getAmplitude(),'\n',
                  'Angle',          ev.getAngle(),'\n',
                  'AverageVelocity',ev.getAverageVelocity(),'\n',
                  'PeakVelocity',   ev.getPeakVelocity(),'\n',
                  'StartTime',      ev.getStartTime(),'\n',
                  'StartGaze',      ev.getStartGaze(),'\n',
                  'StartHREF',      ev.getStartHREF(),'\n',
                  'StartPPD',       ev.getStartPPD(),'\n',
                  'StartVelocity',  ev.getStartVelocity(),'\n',
                  'EndTime',        ev.getEndTime(),'\n',
                  'EndGaze',        ev.getEndGaze(),'\n',
                  'EndHREF',        ev.getEndHREF(),'\n',
                  'StartPPD',       ev.getStartPPD(),'\n',
                  'EndVelocity',    ev.getEndVelocity(),'\n',
                  'Eye',            ev.getEye(),'\n',
                  'Time',           ev.getTime(),'\n',
                  'Type',           ev.getType(), '\n')
     
tk.stopRecording() # stop recording
tk.closeDataFile() # close EDF data file on the Host
tk.receiveDataFile('ev_test.edf', 'ev_test.edf') # retrieve EDF from Host
tk.close() #close the link to the tracker
