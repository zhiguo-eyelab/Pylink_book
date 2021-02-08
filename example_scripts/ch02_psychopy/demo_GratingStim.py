#!/usr/bin/env python3
#
# Filename: demo_GratingStim.py
# Author: Zhiguo Wang
# Date: 2/7/2021
#
# Description:
# The GratingStim() function in PsychoPy

from psychopy import visual, core
import numpy as np

# Open a window
win = visual.Window(size=(600, 400), units="pix", color=[0, 0, 0])

# Prepare the stimuli in memory
grating = visual.GratingStim(win, tex='sqr', mask=None,
                             size=128, sf=1/32.0, pos=(-200, 100))
gabor = visual.GratingStim(win, tex='sin', mask='gauss',
                           size=128, sf=1/32.0, pos=(0, 100))
checker = visual.GratingStim(win, tex='sqrXsqr', mask='circle',
                             size=128, sf=1/32.0, pos=(200, 100))
# Customize texture
# a 8 x 8 grid of random values between -1 and 1
custom_texture = np.random.random((8, 8))*2 - 1
numpy_texture = visual.GratingStim(win, tex=custom_texture, mask=None,
                                   size=128, pos=(-200, -100))
# Use an image as the texture
image_texture = visual.GratingStim(win, tex='texture.png', mask='raisedCos',
                                   size=128, pos=(0, -100))
# You get a rectangle with no texture or mask
no_texture = visual.GratingStim(win, tex=None, mask=None,
                                size=128, pos=(200, -100))

# Show the stimuli
grating.draw()
gabor.draw()
checker.draw()
numpy_texture.draw()
image_texture.draw()
no_texture.draw()
win.flip()

# Take a screenshot and save it to a PNG
win.getMovieFrame()
win.saveMovieFrames('gratings.png')

# Show the stimuli for 5 seconds, then close the window and quit PsychoPy
core.wait(5.0)
win.close()
core.quit()

