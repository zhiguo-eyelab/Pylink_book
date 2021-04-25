#!/usr/bin/env python3
#
# Filename: trial_recycle.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# This demo shows how to recycle a trial

import random
from psychopy import visual, event, core

win = visual.Window(size=(600, 400), units='pix')

def run_trial(trial_id):
    """a simple function to run a single trial"""

    # Show some info on the screen
    task_instruction = f'This is Trial: {trial_id}\n\n' + \
                       'RIGHT--> Next trial\n' + \
                       'LEFT--> Recycle current trial'
    msg = visual.TextStim(win, text=task_instruction)
    msg.draw()
    win.flip()

    # wait for a response
    key = event.waitKeys(keyList=['left', 'right'])

    # clear the window
    win.clearBuffer()
    win.flip()
    core.wait(0.5)

    if 'right' in key:
        return False
    if 'left' in key:
        return True

trial_list = ['t1', 't2', 't3', 't4', 't5']

# Recycle trials with a while-loop
while len(trial_list) > 0:
    # randomize the trial list
    random.shuffle(trial_list)
    
    # grab the last trial and pop it out the trial_list
    trial_to_test = trial_list.pop()

    # run a single trial
    should_recycle = run_trial(trial_to_test)

    # add the trial back to the trial_list if the
    # return value is True (i.e., need to recycle)
    if  should_recycle:
        trial_list.append(trial_to_test)

    # show what trials are left in the trial list
    print(f'The trial you just completed is: {trial_to_test}')
    print(f'Trials left in the list: {trial_list}')

# Close the window and quit PsychoPy
win.close()
core.quit()
