# Filename: fixation_trigger.py

import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors
from math import hypot

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open an EDF data file on the Host PC
tk.openDataFile('psychopy.edf')

# Ensure all types of events are available over the link,
# especially FIXUPDATE
tk.sendCommand('link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT')

# Open a Psychopy window
scn_width, scn_height = (800, 600)
# set monitor parameters 
mon = monitors.Monitor('myMac15', width=53.0, distance=70.0)
mon.setSizePix((scn_width, scn_height))
win = visual.Window((scn_width, scn_height), monitor=mon, fullscr=False, \
                    color=[0,0,0], units='pix', allowStencil=True)

# Use the PsychoPy window for calibration
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# Calibrate the tracker
prompt = 'Press ENTER twice to calibrate the tracker'
calib_prompt = visual.TextStim(win, text=promp)
calib_prompt.draw()
win.flip()
event.waitKeys()
tk.doTrackerSetup()

# Run 3 trials in a for-loop; in each trial, first show a fixation dot,
# wait for the participant to gaze at the fixation dot, then present an
# image for 2 secs
for i in range(2):
    # Load and stretch the background image to fill up the screen
    img = visual.ImageStim(win, image='woods.jpg', \
                           size=(scn_width, scn_height))
    # fixation dot
    fix = visual.GratingStim(win, tex='None',mask='circle', size=30.0)

    # start recording
    tk.startRecording(1,1,1,1)
    # wait for 50 to cache some samples
    pylink.pumpDelay(50) 
    
    # show the fixation dot at the start of a new trial
    fix.draw()
    win.flip()
    
    # fixation trigger - wait for gaze on the fixation dot (for 
    # a minimum of 300 ms)
    fix_dot_x, fix_dot_y = (400, 300) # position of the fixation dot
    triggered = False
    fixation_start_time = -32768
    while not triggered:
        # check if any new events are available
        dt = tk.getNextData()
        if dt > 0:
            ev = tk.getFloatData()
            if dt == pylink.FIXUPDATE:
                # update the fixation start time
                if fixation_start_time < 0:
                    fixation_start_time = ev.getStartTime()
                    
                # how much time has elapsed within the current fixation
                fixation_duration = ev.getEndTime() - fixation_start_time
                
                # check if the average gaze position
                gaze_x, gaze_y = ev.getAverageGaze()
                gaze_error = hypot(gazeX-fix_dot_x, gazeY-fix_dot_y)
                
                # 1 deg = ? pixels in the current fixation
                ppd = (ev.getStartPPD() + ev.getEndPPD())/2.0
                
                # trigger if the duration of the fixation is > 300 ms and
                # the gaze position is close to the fixation dot (< 1.5 deg)
                if fixation_duration >= 300 and gaze_error < ppd*1.5:
                    triggered = True

    # draw the image on the screen for 2 secs
    img.draw()
    win.flip()
    core.wait(2.0)
    
    # clear the screen
    win.color = (0,0,0)
    win.flip()
    core.wait(0.5)
    
    # stop recording
    tk.stopRecording()

# close EDF and the link
tk.closeDataFile()

#close the link to the tracker
tk.close()

# close the graphics
win.close()
core.quit()
