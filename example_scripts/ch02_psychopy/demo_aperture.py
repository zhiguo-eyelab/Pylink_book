# Filename: demo_aperture.py
# Author: Zhiguo Wang
# Date: 11/26/2020
#
# Description:
# Simulating a macular degeneration condition in PsychoPy

from psychopy import visual, core, event

# Open a window
win = visual.Window(size=(800, 600), units="pix", fullscr=False,
                    color=[0, 0, 0], allowStencil=True)

# Create an aperture of arbitray shape
vert = [(0.1, .50), (.45, .20), (.10, -.5), (-.60, -.5), (-.5, .20)]
apt = visual.Aperture(win, size=200, shape=vert, inverted=True)
apt.enabled = True

# Initialize a mouse object
mouse = event.Mouse(visible=False)

# Prepare the stimuli
text = visual.TextStim(win, text="Moving window example by Zhiguo "*24,
                       height=30, color='black', wrapWidth=760)

# Mouse-contingent moving window
while not event.getKeys():
    apt.pos = mouse.getPos()
    text.draw()
    win.flip()

# Quit PsychoPy
win.close()
core.quit()

