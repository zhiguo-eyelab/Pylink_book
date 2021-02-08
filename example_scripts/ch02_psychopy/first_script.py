#!/usr/bin/env python3
#
# Filename: first_script.py
# Author: Zhiguo Wang
# Date: 2/7/2021
#
# Description:
# A short but functioning script in PsychoPy

from psychopy import visual, core, event, monitors

# Set up the monitor parameters, so we can use 'deg' as the screen units
mon_mac15 = monitors.Monitor("mac15", distance=57.0, width=32.0)
mon_mac15.setSizePix([1280, 800])

# Open a window
win = visual.Window([800, 600], monitor=mon_mac15, units="deg")

# Prepare a Gabor in memory
gabor = visual.GratingStim(win, tex="sin", mask="gauss", size=6.0, ori=45.0)

# Draw the Gabor on screen and wait for a key press
while not event.getKeys():
    # Draw the Gabor on screen
    gabor.draw()
    win.flip()

    # Update the phase of the Gabor following each screen refresh
    gabor.phase += 0.05

# close the window and quit PsychoPy
win.close()
core.quit()
