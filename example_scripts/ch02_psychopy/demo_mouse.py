#!/usr/bin/env python3
#
# Filename: demo_mouse.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# A short demo illustrating the various mouse functions in PsychoPy

from psychopy import visual, event, core

# Open a window
win = visual.Window(size=(800, 600), winType='pyglet', units='pix')

# Create a Mouse object
mouse = event.Mouse(visible=True, win=win)

# Prepare the stimuli in memory
text_prompt = visual.TextStim(win=win, text='Do you like PsychoPy?',
                              height=30, pos=(0, 250))
text_yes = visual.TextStim(win=win, text='YES', height=30,
                           pos=(-200, 150), color='red')
text_no = visual.TextStim(win=win, text='NO',  height=30,
                          pos=(200, 150), color='green')
circle_yes = visual.Polygon(win=win, edges=32, radius=60,
                            pos=(-200, 150), fillColor='white')
circle_no = visual.Polygon(win=win, edges=32, radius=60,
                           pos=(200, 150), fillColor='white')
fix_cross = visual.TextStim(win=win, text='+', height=30, pos=(0, -150))
mouse_traj = visual.ShapeStim(win=win, lineColor='black',
                              closeShape=False, lineWidth=5)

# Clear cached events
event.clearEvents()

# Set the mouse position, so the movement starts from the fixation cross
mouse.setPos((0, -150))

# Use a list to store the mouse position
traj = [mouse.getPos()]

# In a while loop, check if the "yes" or "no" circle has been clicked
while not (mouse.isPressedIn(circle_no) or mouse.isPressedIn(circle_yes)):
    # Following a position change, add the new mouse position to 'traj'
    if mouse.mouseMoved():
        traj.append(mouse.getPos())

    # Put stimuli on display and draw the mouse trajectory
    text_prompt.draw()
    circle_no.draw()
    circle_yes.draw()
    text_no.draw()
    text_yes.draw()
    fix_cross.draw()
    mouse_traj.vertices = traj  # this can be slow
    mouse_traj.draw()
    win.flip()

# Close the window and quit PsychoPy
win.close()
core.quit()
