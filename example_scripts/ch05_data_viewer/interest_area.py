# Filename: interest_area.py
import pylink

# connect to the tracker
tk = pylink.EyeLink()

# open an EDF on the Host
tk.openDataFile('seg.edf')

# run through five trials
for trial in range(1,6):
    #print a message to show the current trial #
    print("Trial #: %d" % trial)
    
    # log a TRIALID message to mark trial start
    tk.sendMessage('TRIALID %d' % trial)
    
    tk.startRecording(1,1,1,1) # start recording

    # interest area definitions
    tk.sendMessage('!V IAREA ELLIPSE 1 0 0 100 100 head')
    tk.sendMessage('!V IAREA RECTANGLE 2 85 85 285 185 body')
    tk.sendMessage('!V IAREA FREEHAND 3 285,125 385,50 335,125 tail')
    
    pylink.pumpDelay(2000) # record for 2-sec
    tk.stopRecording() # stop recording
    
    # store trial variables in the EDF data file
    tk.sendMessage('!V TRIAL_VAR condition step')
    tk.sendMessage('!V TRIAL_VAR gap_duration 200')
    tk.sendMessage('!V TRIAL_VAR direction Right')

    # send the TRIAL_RESULT message to mark the end of a trial
    tk.sendMessage('TRIAL_RESULT 0')

# retrieve data file
tk.receiveDataFile('seg.edf', 'seg.edf')

# close the link
tk.close()
