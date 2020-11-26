# Filename: demo_PsychHID.py
# Author: Zhiguo Wang
# Date: 11/26/2020
#
# Description:
# Using PsychHID to register keyboard events in PsychoPy

from psychopy.hardware import keyboard
from psychopy import core, visual

win = visual.Window((200, 200))

# Create a keyboard object
kb = keyboard.Keyboard()

# We define a function to print out the key presses
def waitKey():
    ''' a function to detect a single keypress'''

    got_key = False
    while not got_key:
        keys = kb.getKeys()
        if keys:
            for key in keys:
                print(key.name, key.duration, key.rt, key.tDown)
            got_key = True

# A simple response time task
# Change the window color following each key press
for i in range(10):
    win.color = (i % 2 * 1.0, -1, -1)
    win.flip()
    kb.clearEvents()
    kb.clock.reset()  # reset the clock
    waitKey()
    
# Quit PsychoPy
win.close()
core.quit()
