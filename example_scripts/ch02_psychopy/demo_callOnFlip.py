#!/usr/bin/env python3
#
# Filename: demo_callOnFlip.py
# Author: Zhiguo Wang
# Date: 2/7/2021
#
# Description:
# Check the timing accuracy of the .callonFlip() function

from psychopy import visual, core

win = visual.Window(size=[1200, 800], units="pix", fullscr=True)

# A function to print out the current time
def print_time():
    current_t = core.getTime()
    print(f'print_time() was executed at time: {current_t:.3f}')

# In a for-loop, check if print_time() is executed at the same time as
# the window flip
for i in range(10):
    win.callOnFlip(print_time)
    flip_t = win.flip()
    print(f'Actual window flipping time was: {flip_t:.3f}')
    core.wait(0.5)

# Close the window and quit PsychoPy
win.close()
core.quit()
