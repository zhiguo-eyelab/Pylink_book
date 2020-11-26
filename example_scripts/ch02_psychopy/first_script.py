# Filename: first_script.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# A short but functioning script in PsychoPy

from psychopy import visual, core, event, monitors

# Set monitor parameters
mon_mac15 = monitors.Monitor("mac15", distance=57.0, width=32.0)
mon_mac15.setSizePix([1920, 1080])

# Open a window
win = visual.Window([800, 600], monitor=mon_mac15, units="deg")

# Prepare a Gabor in memory
gabor = visual.GratingStim(win, tex="sin", mask="gauss", size=6.0, ori=45.0)

# Draw the Gabor on screen and wait for a key press
while True:
    # Break out the loop if a key is pressed
    key = event.getKeys()
    if len(key) > 0:
        win.close()
        core.quit()

    # Draw the Gabor on screen
    gabor.draw()
    win.flip()

    # Update the phase of the Gabor following each screen refresh
    gabor.phase += 0.1


