# Filename: gc_window.py

import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors

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

# make sure sample data is available over the link 
tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT")

# show instructions and calibrate the tracker
instructions = visual.TextStim(win, text='Press ENTER twice to calibrate the tracker')
instructions.draw()
win.flip()
event.waitKeys()
tk.doTrackerSetup()

# set up a circular aperture as the gaze-contingent window
gaze_window = visual.Aperture(win, size=200)
gaze_window.enabled=True

# load and stretch the background image to fill full screen
img = visual.ImageStim(win, image='sacrmeto.jpg', size=(scnWidth, scnHeight))

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
    gaze_window.pos = (gaze_pos[0]-scnWidth/2, scnHeight/2-gaze_pos[1])
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
