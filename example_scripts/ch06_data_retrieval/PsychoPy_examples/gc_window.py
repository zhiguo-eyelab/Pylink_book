# Filename: gc_window.py

import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Make sure all types of sample data is available over the link 
tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT")

# Open an EDF data file
tk.openDataFile('psychopy.edf')

# Open a window in Psychopy
scn_width, scn_height = (800, 600)
# set monitor parameters 
mon = monitors.Monitor('myMac15', width=53.0, distance=70.0)
mon.setSizePix((scn_width, scn_height))
win = visual.Window((scn_width, scn_height), monitor=mon, fullscr=False,\
                    color=[0,0,0],units='pix', allowStencil=True)

# Use the PsychoPy window to present calibration targets
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# Calibrate the tracker
prompt = 'Press ENTER twice to calibrate the tracker'
calib_prompt = visual.TextStim(win, text=promp)
calib_prompt.draw()
win.flip()
event.waitKeys()
tk.doTrackerSetup()

# Set up a circular aperture and use it as a gaze-contingent window
gaze_window = visual.Aperture(win, size=200)
gaze_window.enabled=True

# Load a background image to fill up the screen
img = visual.ImageStim(win, image='woods.jpg', \
                       size=(scn_width, scn_height))

# start recording
tk.startRecording(1,1,1,1)

# show the image indefinitely until a key is pressed
gaze_pos =  (-32768, -32768)
terminate = False
event.clearEvents() # clear cached (keyboard/mouse etc.) events
while not terminate:
    # check for keypress to terminate a trial
    if event.getKeys():
        terminate = True
        
    # check for new samples
    dt = tk.getNewestSample()
    if dt is not None:
        if dt.isRightSample():
            gaze_pos = dt.getRightEye().getGaze()
        elif dt.isLeftSample():
            gaze_pos = dt.getLeftEye().getGaze()

    # draw background image with the aperture (window)
    img.draw()
    gaze_window.pos = (gaze_pos[0]-scn_width/2, scn_height/2-gaze_pos[1])
    win.flip()

# stop recording
tk.stopRecording()

# close EDF and the link
tk.closeDataFile()

#close the link to the tracker
tk.close()

# close the graphics
win.close()
core.quit()
