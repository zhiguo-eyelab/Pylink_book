# Filename: simple_drawing.py
import pylink

# connect to the tracker
tk = pylink.EyeLink()

# log the screen size for Data Viewer to draw graphics
tk.sendMessage('DISPLAY_SCREEN 0 0 1024 768')

# open an EDF on the Host
tk.openDataFile('seg.edf')

# run through five trials of 2-second recordings
for trial in range(1,6):
    #print a message to show the current trial #
    print("Trial #: %d" % trial)
    
    # the TRIALID message marks the start of a new trial
    tk.sendMessage('TRIALID %d' % trial)
    
    tk.startRecording(1,1,1,1) # start recording
  
    # draw a central fixation flanked by two possible targets
    tk.sendMessage('!V CLEAR 255 255 255') # clear the screen to show white background
    tk.sendMessage('!V FIXPOINT 0 0 0 0 0 0 512 384 25 0') # central fixation dot
    tk.sendMessage('!V FIXPOINT 0 0 0 255 255 255 312 384 80 75') # non-target
    tk.sendMessage('!V FIXPOINT 255 0 0 255 0 0 712 384 80 0') # target

    pylink.pumpDelay(2000) # record for 2-sec
    tk.stopRecording() # stop recording

    # send the TRIAL_RESULT message to mark the end of a trial
    tk.sendMessage('TRIAL_RESULT 0')

# retrieve data file
tk.closeDataFile()
tk.receiveDataFile('seg.edf', 'seg.edf')

# close the link
tk.close()
