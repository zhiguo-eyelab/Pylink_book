# Filename: trial_recycle.py
# Author: Zhiguo Wang
# Date: 11/26/2020
#
# Description:
# This demo shows how to recycle a trial

import random
from psychopy import visual, event, core

myWin = visual.Window(size=(600, 400), units='pix')

def run_trial(trial_id):
    """a simple function to run a single trial"""

    # Show some info on the screen
    task_instruction = 'This is Trial: {}\n\n'.format(trial_id) + \
                       'RIGHT--> Next trial\n' + \
                       'LEFT--> Recycle current trial'
    msg = visual.TextStim(myWin, text=task_instruction)
    msg.draw()
    myWin.flip()

    # wait for a response
    key = event.waitKeys(keyList=['left', 'right'])

    # clear the window
    myWin.clearBuffer()
    myWin.flip()
    core.wait(0.5)

    if 'right' in key:
        return False
    if 'left' in key:
        return True

trial_list = ['t1', 't2', 't3', 't4', 't5']

# Recycle trials with a while-loop
while len(trial_list) > 0:

    # randomly select a trial from the trial_list
    trial_to_test = random.choice(trial_list)

    # run a single trial
    should_recycle = run_trial(trial_to_test)

    # remove the trial we just tested from the trial_list if the
    # return value is False (i.e., no need to recycle)
    if not should_recycle:
        trial_list.remove(trial_to_test)

    # show what trials are left in the trial list
    print('Trials left in the list: {}'.format(trial_list))

# Quit Psychopy
myWin.close()
core.quit()
