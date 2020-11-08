# Filename: fixation_trigger.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# A fixation trigger implemented in PsychoPy

import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors
from math import hypot

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open an EDF data file on the Host PC
tk.openDataFile('psychopy.edf')

# Make all types of events  available over the link, especially the
# FIXUPDATE event, which report the current status of a fixation at
# predefined intervals (default: 50 ms)
event_flags = 'LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT'
tk.sendCommand('link_event_filter = %s' % event_flags)

# Open a window in PsychoPy
SCN_WIDTH, SCN_HEIGHT = (800, 600)
# set monitor parameters
mon = monitors.Monitor('myMac15', width=53.0, distance=70.0)
mon.setSizePix((SCN_WIDTH, SCN_HEIGHT))
win = visual.Window((SCN_WIDTH, SCN_HEIGHT), monitor=mon, fullscr=False,
                    color=[0, 0, 0], units='pix', allowStencil=True)

# Use the PsychoPy window to present calibration targets
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# Calibrate the tracker
calib_prompt = 'Press ENTER twice to calibrate the tracker'
calib_msg = visual.TextStim(win, text=promp)
calib_msg.draw()
win.flip()
event.waitKeys()
tk.doTrackerSetup()

# Run 3 trials in a for-loop; in each trial, first show a fixation dot,
# wait for the participant to gaze at the fixation dot, then present an
# image for 2 secs
for i in range(3):
    # Load and stretch the background image to fill up the screen
    img = visual.ImageStim(win, image='woods.jpg',
                           size=(SCN_WIDTH, SCN_HEIGHT))
    # fixation dot
    fix = visual.GratingStim(win, tex='None', mask='circle', size=30.0)

    # Start recording
    tk.startRecording(1, 1, 1, 1)
    # wait for 50 to cache some samples
    pylink.msecDelay(50)

    # Show the fixation dot at the start of a new trial
    fix.draw()
    win.flip()

    # fixation trigger - wait for gaze on the fixation dot (for
    # a minimum of 300 ms)
    # fixation dot position in reference to the top-left screen corner
    fix_dot_x, fix_dot_y = (SCN_WIDTH/2.0, SCN_HEIGHT/2.0)
    triggered = False
    fixation_start_time = -32768
    while not triggered:
        # Check if any new events are available
        dt = tk.getNextData()
        if dt > 0:
            ev = tk.getFloatData()
            if dt == pylink.FIXUPDATE:
                # Update the fixation start time
                if fixation_start_time < 0:
                    fixation_start_time = ev.getStartTime()

                # How much time has elapsed within the current fixation
                fixation_duration = ev.getEndTime() - fixation_start_time

                # Check if the average gaze position
                gaze_x, gaze_y = ev.getAverageGaze()
                gaze_error = hypot(gaze_x-fix_dot_x, gaze_y-fix_dot_y)

                # 1 deg = ? pixels in the current fixation
                ppd = (ev.getStartPPD() + ev.getEndPPD())/2.0

                # Break if the duration of the fixation is > 300 ms and
                # the gaze position is close to the fixation dot (< 1.5 deg)
                if fixation_duration >= 300 and gaze_error < ppd*1.5:
                    triggered = True

    # Show the image for 2 secs
    img.draw()
    win.flip()
    core.wait(2.0)

    # Clear the screen
    win.color = (0, 0, 0)
    win.flip()
    core.wait(0.5)

    # Stop recording
    tk.stopRecording()

# Close the EDF data file on the Host
tk.closeDataFile()

# Close the link to the tracker
tk.close()

# Close the graphics
core.quit()
