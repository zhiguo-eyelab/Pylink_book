# Filename: keyboard_PsychHID.py

from psychopy.hardware import keyboard
from psychopy import core, visual

win = visual.Window((200,200))

# create a keyboard evice
kb = keyboard.Keyboard()

def waitKey():
    ''' a function to detect a single key press'''
    got_key = False
    while not got_key:
        keys = kb.getKeys()
        if keys:
            for key in keys:
                print(key.name, key.duration, key.rt, key.tDown)
            got_key = True
            
for i in range(10):
    win.color = (i%2*1.0, -1, -1)
    win.flip()
    kb.clock.reset() # reset the clock
    kb.clearEvents()
    waitKey()
