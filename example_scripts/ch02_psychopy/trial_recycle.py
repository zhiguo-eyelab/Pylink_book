# Filename: trial_recycle.py

import random
from psychopy import visual, event, core

myWin = visual.Window(size=(600,400), units ='pix')

def run_trial(trial_id):
    """a simple function to run a single trial"""
    
    # show some info on the screen
    msg1 = visual.TextStim(myWin, text='This is Trial----{}'.format(trial_id), pos=(0,100))    
    msg2 = visual.TextStim(myWin, text='RIGHT--> Next trial; LEFT--> Recycle current trial')
    msg1.draw(); msg2.draw()
    myWin.flip()
    
    # wait for a response
    key = event.waitKeys(keyList=['left', 'right'])
    
    # clear the window
    myWin.clearBuffer()
    myWin.flip()
    core.wait(0.5)

    if 'right' in key: 
        recycle = False
    if 'left' in key:
        recycle = True
        
    return recycle
    
trial_list = ['t1', 't2', 't3', 't4', 't5']

# recycle trials with a while loop
while len(trial_list) > 0: 
    
    # randomly select a trial from the trial_list
    trial_to_test = random.choice(trial_list)
    
    # run a single trial, the return value of run_trial could be True or False
    should_recycle = run_trial(trial_to_test)
    
    # remove the trial we just tested from the list if the return value is False
    # (i.e., no need to recycle)
    if should_recycle == False:
        trial_list.remove(trial_to_test)

    # show what trials are left in the trial list
    print('Trials left in the list: {}'.format(trial_list))

# quit psychopy
core.quit()
