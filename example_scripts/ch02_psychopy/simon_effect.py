# Filename: simon_effect.py

import random
from psychopy import visual, core, event, gui

# open a window and create stimuli
win = visual.Window((1024, 768), units='pix', fullscr=False, color='black')
text_msg = visual.TextStim(win, text='message')
tar_stim = visual.GratingStim(win, tex='None', mask='circle', size=60.0)

# possible target position
tar_pos = {'left': (-200, 0), 'right':(200, 0)}

# trial list
trials = [['left', 'red', 'z', 'congruent'],
          ['left', 'blue', 'slash', 'incongruent'],
          ['right', 'red', 'z', 'incongruent'],
          ['right', 'blue', 'slash', 'congruent']]

def run_trial(trial_pars, data_file, participant):
    """ Run a single trial.
    
    trial_pars -- target position, color and correct key, e.g., ['left', 'red', 'z', 'cong']
    data_file -- an file to save trial data
    participant -- information about the participant in a dictionary, {'id':1, 'name':zw}"""
    
    pos, color, cor_key, congruency = trial_pars # upacking the parameter list
    tar_stim.pos = tar_pos[pos] # set target postion
    tar_stim.color = color # set target color

    # present the fixation for 750 ms
    text_msg.text = '+'
    text_msg.draw()
    win.flip()
    core.wait(0.750)

    # present the target and wait for a key response
    tar_stim.draw()
    win.flip()
    t_tar_onset = core.getTime()
    tar_resp = event.waitKeys(1500, ['z', 'slash'],timeStamped=True)

    # write data to file 
    trial_data = list(participant.values()) + trial_pars +[t_tar_onset] + list(tar_resp[0])
    trial_data = map(str, trial_data) # convert to string
    data_file.write(','.join(trial_data) + '\n')
    
    # clear the screen and set an ITI of 500 ms
    win.color = 'black'
    win.flip()
    core.wait(0.500)

# -- real experiment starts here --
# get participant info from a dialog
participant = {'Participant ID': 0, 'Participant Initials': 'zw'}
dlg = gui.DlgFromDict(participant, title='Enter participant info here')

# open a data file with write permission
d_file = open(participant['Participant Initials']+'.csv', 'w')

# show the task instructions
text_msg.text = 'Press Z to RED\nPress / to BLUE\n\nPress <SPACE> to start'
text_msg.draw()
win.flip()
event.waitKeys(keyList=['space'])

# randomly shuffle the trial list and iterate over all of them
random.seed = 1000
test_trials = trials[:]*2
random.shuffle(test_trials)
for pars in test_trials:
    run_trial(pars, d_file, participant)

# close data file
d_file.close()

# exit
core.quit()

