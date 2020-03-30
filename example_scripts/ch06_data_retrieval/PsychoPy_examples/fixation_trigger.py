# Filename: fixation_trigger.py

import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors
from math import hypot

# established a link to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open an EDF data file
tk.openDataFile('psychopy.edf')

# Initialize custom graphics in Psychopy
scnWidth, scnHeight = (800, 600)
# set monitor parameters 
mon = monitors.Monitor('myMac15', width=53.0, distance=70.0)
mon.setSizePix((scnWidth, scnHeight))
win = visual.Window((scnWidth, scnHeight), monitor=mon, fullscr=False, color=[0,0,0],
                    units='pix', allowStencil=True)
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# make sure all types of event data are available over the link
tk.sendCommand('link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT')

# show instructions and calibrate the tracker
instructions = visual.TextStim(win, text='Press ENTER twice to calibrate the tracker')
instructions.draw()
win.flip()
event.waitKeys()
tk.doTrackerSetup()

# load and stretch the background image to fill full screen
img = visual.ImageStim(win, image='sacrmeto.jpg', size=(scnWidth, scnHeight))
# prepare a fixation dot in the RAM
fix = visual.GratingStim(win, tex='None',mask='circle', size=30.0)

# run 3 trials in a for-loop; in each trial, show a fixation dot first; wait for
# the participant to gaze at the fixation dot, then present an image for 2 secs
for i in range(2):
    
    # start recording
    tk.startRecording(1,1,1,1)
    # wait for 100 to cache some samples
    pylink.pumpDelay(100) 
    
    # show the fixation dot at the start of a new trial
    fix.draw()
    win.flip()
    
    # fixation trigger - wait for gaze on the fixation dot (for 
    # a minimum of 300 ms)
    fixDotX, fixDotY = (400, 300) # position of the fixation dot
    triggered = False
    fixationStartTime = -1
    while not triggered:
        # check if any new events are available
        dt = tk.getNextData()
        if dt > 0:
            ev = tk.getFloatData()
            if dt == pylink.FIXUPDATE:
                # update the fixation start time
                if fixationStartTime < 0:
                    fixationStartTime = ev.getStartTime()
                    
                # how much time has elapsed within the current fixation
                fixDuration = ev.getEndTime() - fixationStartTime
                
                # check if the average gaze position
                gazeX, gazeY = ev.getAverageGaze()
                gazeError = hypot(gazeX-fixDotX, gazeY-fixDotY)
                
                # trigger if the duration of the fixation is > 300 ms and
                # the gaze position is close to the fixation dot (< 30 pixels)
                if fixDuration >= 300 and gazeError < 30.0:
                    triggered = True

    # draw the image on the screen for 2 secs
    img.draw()
    win.flip()
    core.wait(2.0)
    
    # clear the screen
    win.color = (0,0,0)
    win.flip()
    core.wait(1.5)
    
    # stop recording
    tk.stopRecording()

# close EDF and the link
tk.closeDataFile()

#close the link to the tracker
tk.close()

# close the graphics
win.close()
core.quit()
