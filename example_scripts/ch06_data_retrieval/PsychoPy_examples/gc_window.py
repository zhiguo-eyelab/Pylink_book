# Filename: gc_window.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# A gaze-contingent window task implemented in PsychoPy

import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Make all types of sample data available over the link
sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT'
tk.sendCommand('link_sample_data  = %s' % sample_flags)

# Open an EDF data file
tk.openDataFile('psychopy.edf')

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

# Set up a circular aperture and use it as a gaze-contingent window
gaze_window = visual.Aperture(win, size=200)
gaze_window.enabled = True

# Load a background image to fill up the screen
img = visual.ImageStim(win, image='woods.jpg',
                       size=(SCN_WIDTH, SCN_HEIGHT))

# start recording
tk.startRecording(1, 1, 1, 1)

# show the image indefinitely until a key is pressed
gaze_pos = (-32768, -32768)
terminate = False
event.clearEvents()  # clear cached PsychoPy events
while not terminate:
    # Check for keypress to terminate a trial
    if event.getKeys():
        terminate = True

    # Check for new samples
    dt = tk.getNewestSample()
    if dt is not None:
        if dt.isRightSample():
            gaze_pos = dt.getRightEye().getGaze()
        elif dt.isLeftSample():
            gaze_pos = dt.getLeftEye().getGaze()

    # Draw the background image
    img.draw()
    # Update the window with the current gaze position
    gaze_window.pos = (gaze_pos[0]-SCN_WIDTH/2,
                       SCN_HEIGHT/2-gaze_pos[1])
    win.flip()

# Stop recording
tk.stopRecording()

# Close EDF and the link
tk.closeDataFile()

# Close the link to the tracker
tk.close()

# Close the graphics
core.quit()
