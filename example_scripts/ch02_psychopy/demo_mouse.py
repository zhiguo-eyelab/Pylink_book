# Filename: mouse_demo.py

from psychopy import visual, event, core

# open a window and instantiate a mouse object
win = visual.Window(size=(800, 600), winType='pyglet', units ='pix', colorSpace='rgb')
mouse = event.Mouse(visible=True)

# prepare the visuals
msg = visual.TextStim(win=win, text='Do you like PsychoPy?', height = 30, pos=(0, 250))
dis = visual.TextStim(win=win, text='YES', height = 30, pos=(-200,150), color='red')
agr = visual.TextStim(win=win, text='NO',  height = 30, pos=(200, 150), color='green')
fix = visual.TextStim(win=win, text='+', height = 30, pos=(0, -150))
dis_box = visual.Polygon(win=win, edges=32, radius=60, pos=(-200,150), fillColor='white')
agr_box = visual.Polygon(win=win, edges=32, radius=60, pos=(200,150), fillColor='white')
mouse_traj = visual.ShapeStim(win=win, lineColor='black', closeShape=False, lineWidth=5)

# use a while loop to wait for a mouse click and show the mouse trajectory
event.clearEvents()
mouse.setPos((0,-150))
traj = [mouse.getPos()] # need to call this function to update the mouse position
while not (mouse.isPressedIn(dis_box) or mouse.isPressedIn(agr_box)):
    # if the mouse has been moved, add the new position in 'traj'
    if mouse.mouseMoved(): 
        traj.append(mouse.getPos())
        
    # put stimuli on display and draw the mouse trajectory
    msg.draw(); dis_box.draw(); agr_box.draw()
    dis.draw();agr.draw(); fix.draw()
    mouse_traj.vertices = traj # this can be slow
    mouse_traj.draw()
    win.flip()
    
# quit PsychoPy
win.close()
core.quit()
