# Filename: demo_callOnFlip.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# Check the the timing accuracy of the .callonFlip() function

from psychopy import visual, core

win = visual.Window(size=[800, 600], units="pix")

# A function to print out the current time
def print_time():
    current_t = core.getTime()
    print('print_time() was executed at time: %.3f' % current_t)

# In a for-loop, check if print_time() is executed at the same time as
# the window flip
for i in range(10):
    win.callOnFlip(print_time)
    flip_t = win.flip()
    print('Actual flipping time: %.3f' % flip_t)
    core.wait(0.5)

# Quit PsychoPy
win.close()
core.quit()
