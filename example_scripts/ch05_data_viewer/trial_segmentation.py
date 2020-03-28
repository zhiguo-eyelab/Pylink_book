# Filename: trial_segmentation.py
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
    pylink.pumpDelay(2000) # record for 2-sec
    tk.stopRecording() # stop recording
    
    # log a TRIAL_RESULT message to mark trial ends
    tk.sendMessage('TRIAL_RESULT 0')

# close data file and retrieve
tk.closeDataFile()
tk.receiveDataFile('seg.edf', 'seg.edf')

# close the link
tk.close()
