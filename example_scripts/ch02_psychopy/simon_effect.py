#!/usr/bin/env python3
#
# Filename: simon_effect.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# Measuring the Simon effect in PsychoPy

import random
from psychopy import visual, core, event, gui

# Open a window and prepare the stimuli
win = visual.Window((1280, 800), units='pix', fullscr=False, color='black')
text_msg = visual.TextStim(win, text='message')
tar_stim = visual.GratingStim(win, tex='None', mask='circle', size=60.0)

# Possible target position
tar_pos = {'left': (-200, 0), 'right': (200, 0)}

# A list of all possible trial parameter combinations
trials = [
    ['left', 'red', 'z', 'congruent'],
    ['left', 'blue', 'slash', 'incongruent'],
    ['right', 'red', 'z', 'incongruent'],
    ['right', 'blue', 'slash', 'congruent']
    ]


def run_trial(trial_pars, data_file, participant):
    """ Run a single trial.

    trial_pars -- target position, color, and correct key, e.g.,
                  ['left', 'red', 'z', 'cong']
    data_file -- a file to save trial data
    participant -- information about the participant in a dictionary,
                  {'id':1, 'name':zw}"""

    # Unpacking the parameter list
    pos, color, cor_key, congruency = trial_pars

    # Set target position and color
    tar_stim.pos = tar_pos[pos]
    tar_stim.color = color

    # Present a fixation cross for 750 ms
    text_msg.text = '+'
    text_msg.draw()
    win.flip()
    core.wait(0.750)

    # Present the target and wait for a key response
    tar_stim.draw()
    win.flip()
    t_tar_onset = core.getTime()
    tar_resp = event.waitKeys(1500, ['z', 'slash'], timeStamped=True)

    # write data to file
    trial_data = list(participant.values()) + \
        trial_pars + [t_tar_onset] + \
        list(tar_resp[0])
    trial_data = map(str, trial_data)  # convert list items to string
    data_file.write(','.join(trial_data) + '\n')

    # clear the screen and set an ITI of 500 ms
    win.color = 'black'
    win.flip()
    core.wait(0.500)

# ------ Real experiment starts here -------

# Get participant info with a dialog
participant = {'Participant ID': 0, 'Participant Initials': 'zw'}
dlg = gui.DlgFromDict(participant, title='Enter participant info here')

# Open a data file with write permission
d_file = open(participant['Participant Initials']+'.csv', 'w')

# Show task instructions
text_msg.text = 'Press Z to RED\nPress / to BLUE\n\nPress <SPACE> to start'
text_msg.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Randomly shuffle the trial list and iterate over all of them
random.seed = 1000  # Set a random seed
trial_list = trials[:]*2
random.shuffle(trial_list)
for pars in trial_list:
    run_trial(pars, d_file, participant)

# Close the data file
d_file.close()

# Close the window and quit PsychoPy
win.close()
core.quit()

