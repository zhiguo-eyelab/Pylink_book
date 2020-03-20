# Filename: demo_GratingStim.py

from psychopy import visual, core
import numpy as np

# open a window
win = visual.Window(size=(600,400), units="pix", fullscr=False, color=[0,0,0])

# prepare the stimuli
grating = visual.GratingStim(win, tex='sqr', mask=None, size=128, sf = 1./32, pos=(-200,100))
gabor = visual.GratingStim(win, tex='sin', mask='gauss', size=128, sf =1./32, pos=(0,100))
checker = visual.GratingStim(win, tex='sqrXsqr', mask='circle', size=128, sf=1./32, pos=(200,100))
# custom texture (random value on gray scale)
custom_tex = np.random.random((8,8))*2-1 # a 8 x 8 grid of values between -1 and 1
numpy_texture = visual.GratingStim(win, tex=custom_tex, mask=None, size=128, pos=(-200,-100))
# image as texture
image_texture = visual.GratingStim(win, tex='texture.png', mask='raisedCos', size=128, pos=(0,-100))
no_texture = visual.GratingStim(win, tex=None, mask=None, size=128, pos=(200,-100))

# show the stimuli
grating.draw()
gabor.draw()
checker.draw()
numpy_texture.draw()
image_texture.draw()
no_texture.draw()
win.flip()
win.getMovieFrame()
win.saveMovieFrames('gratings.png')

# wait for 5 seconds and close the window
core.wait(5)
win.close()
core.quit()

