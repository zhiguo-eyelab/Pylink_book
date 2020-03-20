# Filename: demo_aperture.py

from psychopy import visual, core, event

# create a window
win = visual.Window(size=(800,600), units="pix", fullscr=False,
                    color=[0,0,0], allowStencil=True)

# create an aperture
#apt = visual.Aperture(win, size=300, shape='circle', inverted=True)
vert = [(0.1, .50), (.45, .20), (.10,-.5), (-.60, -.5), (-.5,.20)]
apt = visual.Aperture(win, size=200, shape=vert, inverted=True)
apt.enabled = True

#create a mouse instance
mouse = event.Mouse(visible=False)

# prepare the stimuli
text = visual.TextStim(win, text="Moving window example by Zhiguo"*24,
                       height=30,color='black', wrapWidth=760) 

# mouse-contingent moving window
while not event.getKeys():
    apt.pos = mouse.getPos() 
    text.draw()
    win.flip()
    win.getMovieFrame()
    win.saveMovieFrames('aperture_demo.png')

# quit PsychoPy
win.close()
core.quit()

