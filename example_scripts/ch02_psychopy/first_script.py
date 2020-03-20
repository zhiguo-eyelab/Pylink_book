# Filename: first_script.py

from psychopy import visual, core, event, monitors

# set monitor parameters
mon_mac15 = monitors.Monitor("mac15", distance=57.0, width=32.0)
mon_mac15.setSizePix([1920,1080])

# open a window
win = visual.Window([800,600], monitor=mon_mac15, units="deg")

# prepare the Gabor
gabor = visual.GratingStim(win, tex="sin", mask="gauss", size=6.0, ori=45.0)

# draw the Gabor on the display and wait for key responses.
while True:
    gabor.phase += 0.1
    gabor.draw()
    win.flip()
    key = event.getKeys()
    if len(key)>0: # press any key to quit
        win.close()
        core.quit()