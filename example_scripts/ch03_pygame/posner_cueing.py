# Filename: posner_cueing.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# A Posner cueing task implemented in Pygame

import random
import pygame
import sys
from pygame import display, draw, Rect, time, event, key, mouse
from pygame.locals import *

# Set a few constants
sz = 90  # size of the placeholder
colors = {'gray': (128, 128, 128),
          'white': (255, 255, 255),
          'black': (0, 0, 0)}
pos = {'left': (212, 384),
       'center': (512, 384),
       'right': (812, 384)}

# List of all unique trials, [cue_pos, tar_pos, isi, cueing, cor_key]
trials = []
for cue_pos in ['left', 'right']:
    for tar_pos in ['left', 'right']:
        for isi in [0, 100, 300, 700]:
            if cue_pos == tar_pos:
                cueing = 'cued'
            else:
                cueing = 'uncued'
            if tar_pos == 'left':
                cor_key = 'z'
            else:
                cor_key = '/'
            trials.append([cue_pos, tar_pos, isi, cueing, cor_key])


def draw_frame(frame, trial_pars):
    ''' Draw the possible screens.

    frame -- which frame to draw, e.g., 'fix', 'cue', 'target'
    trial_pars -- parameters, [cue_pos, tar_pos, isti, cueing, cor_key]'''

    # Unpack the trial parameters
    cue_pos, tar_pos, isi, cueing, cor_key = trial_pars

    # Clear the screen and fill it with black
    win.fill(colors['black'])

    # The place holders are visible on all screens
    # Here, 'pos' is a dictionary;
    # we retrieve both the key and value pairs in a for-loop
    for key, (x, y) in pos.items():
        # Draw the place holder
        draw.rect(win, colors['gray'], Rect(x - sz/2, y - sz/2, sz, sz), 1)

        # The fixation cross is visible on all screens
        if key == 'center':
            draw.line(win, colors['gray'], (x - 20, y), (x + 20, y), 3)
            draw.line(win, colors['gray'], (x, y - 20), (x, y + 20), 3)

    # Draw the fixation screen-- three placeholders with a cross
    if frame == 'fix':
        pass

    # Draw the cue (a bright box--a Rect)
    if frame == 'cue':
        c_x, c_y = pos[cue_pos]  # coordinates of the cue
        draw.rect(win, colors['white'], Rect(c_x - sz/2, c_y - sz/2,
                                             sz, sz), 5)

    # Draw the target (a filled white disk)
    if frame == 'target':
        draw.circle(win, colors['white'], pos[tar_pos], 20)

    display.flip()


def run_trial(trial_pars, subj_info, data_file):
    ''' Run a single trial.

    trial_pars -- a list specifying trial parameters,
                  [cue_pos, tar_pos, isi, cueing, cor_key]
    subj_info -- info about the subject [id, name, age]
    data_file -- an open file to save the trial data.'''

    # Show the fixation then wait for 1000 ms
    draw_frame('fix', trial_pars)
    time.wait(1000)

    # Show the cue for 100 ms
    draw_frame('cue', trial_pars)
    time.wait(100)

    # Inter-stimulus interval (ISI)
    draw_frame('fix', trial_pars)
    time.wait(trial_pars[2])

    # Show the target and register a keypress response
    draw_frame('target', trial_pars)
    tar_onset = time.get_ticks()
    tar_resp = -32768  # response time
    resp_key = -32768  # key pressed

    # Check for key presses
    time_out = False
    got_key = False
    event.clear()  # clear bufferred events
    while not (time_out or got_key):
        # Cehck for time out (1500 ms)
        if time.get_ticks() - tar_onset > 1500:
            time_out = True

        # Check if any key has been pressed
        for ev in event.get():
            if ev.type == KEYDOWN:
                if ev.key in [K_z, K_SLASH]:
                    tar_resp = time.get_ticks()
                    resp_key = key.name(ev.key)
                    got_key = True

    # write data to file
    trial_data = subj_info + trial_pars + [tar_onset, tar_resp, resp_key]
    trial_data = map(str, trial_data)
    data_file.write(','.join(trial_data) + '\n')

    # ITI (inter-trial_interval)
    draw_frame('fix', trial_pars)
    time.wait(1500)

# -- Real experiment starts from here --
# Get subject info from the Python shell
subj_id = input('Subject ID (e.g., 01): ')
subj_age = input('Subject Age: ')
subj_info = [subj_id, subj_age]

# Open a CSV file to store the data
d_file = open('d_{}.csv'.format(subj_info[0]), 'w')

# Open a window, add the FULLSCREEN flag for precise timing
win = display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF)
# Hide the mouse cursor
mouse.set_visible(False)

# Randomly shuffle the trial list and test them one by one
test_trials = trials[:]*1  # how many trials to test
random.shuffle(test_trials)  # randomize
for pars in test_trials:
    run_trial(pars, subj_info, d_file)

# Close the data files
d_file.close()

# Quit Pygame
pygame.quit()
sys.exit()
