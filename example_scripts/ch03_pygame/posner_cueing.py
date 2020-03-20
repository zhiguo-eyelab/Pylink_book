# Filename: posner_cueing.py

import random, pygame, sys
from pygame import display, draw, Rect, time, event, key
from pygame.locals import *

# constants
sz = 90 # size of the place holder
pos = {'left':(212,384), 'center':(512,384),'right':(812,384)}
colors = {'gray':(128,128,128),'white':(255,255,255),'black':(0,0,0)}

# list of all unique trials, [cue_pos, tar_pos, isi, cueing, cor_key]
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

    frame -- which frame to draw, e.g., 'fix','cue', 'target'
    trial_pars -- parameters, [cue_pos, tar_pos, isti, cueing, cor_key]'''
    
    # unpack the trial parameters
    cue_pos, tar_pos, itiisi, cueing, cor_key = trial_pars

    # clear the screen and fill it with black color
    win.fill(colors['black'])
    
    # the fixation cross and the place holders are always shown visible on all screens
    # 'pos' is a dictionary, in which the key and value pairs can be retrieved on-by-one in a for-loop
    for key, (x, y) in pos.items():
        # draw the place holder
        draw.rect(win, colors['gray'], Rect(x-sz/2, y-sz/2, sz, sz), 1)
        
        # draw the cross with two lines
        if key == 'center':
            draw.line(win, colors['gray'], (x-20,y), (x+20,y), 3)
            draw.line(win, colors['gray'], (x,y-20), (x,y+20), 3)
            
    # draw the fixation screen (do nothing because nothing needs to change)
    if frame == 'fix':
        pass
    
    # draw the cue (a bright box--a Rect)
    if frame == 'cue':
        c_x, c_y = pos[cue_pos] # coordinates of the cue
        draw.rect(win, colors['white'], Rect(c_x-sz/2, c_y-sz/2, sz, sz), 5)
        
    # draw the target (a filled disk)
    if frame == 'target':
        draw.circle(win, colors['white'], pos[tar_pos], 20)
    
    display.flip()


    
def run_trial(trial_pars, subj_info, data_file):
    ''' Run a single trial.

    trial_pars -- a list specifying trial parameters, [cue_pos, tar_pos, isi, cueing, cor_key]
    subj_info -- info about the subject [id, name, age]
    data_file -- an open file to save the trial data.'''
    
    # show the fixation then wait for 1000 ms
    draw_frame('fix', trial_pars)
    time.wait(1000)

    # show the cue for 100 ms
    draw_frame('cue', trial_pars)
    time.wait(100)

    # ISI
    draw_frame('fix', trial_pars)
    time.wait(trial_pars[2])

    # show the target and register a keypress response
    draw_frame('target', trial_pars)
    t_tar_onset = time.get_ticks()
    t_tar_resp = -1 # response time
    t_tar_key = -1 # key pressed

    # check for key presses
    time_out = False
    got_key = False
    event.clear() # clear bufferred events, if there is any
    while not (time_out or got_key):
        if time.get_ticks() - t_tar_onset > 1500:
            time_out = True
            
        # check if any key has been pressed
        for ev in event.get():
            if ev.type == KEYDOWN:
                print(ev.key)
                if ev.key in [K_z, K_SLASH]:
                    t_tar_resp = time.get_ticks()
                    t_tar_key = key.name(ev.key)
                    got_key = True

    # write data to file
    trial_data = subj_info + trial_pars + [t_tar_onset, t_tar_resp, t_tar_key]
    trial_data = map(str, trial_data)
    data_file.write(','.join(trial_data) + '\n')

    # ITI (inter-trial_interval)
    draw_frame('fix', trial_pars)
    time.wait(1500)

# -- real experiment starts from here --
# get subject info from the Python shell
subj_id = input('Subject ID (e.g., 01): ')
subj_age = input('Subject Age: ')
subj_info = [subj_id, subj_age]

# open a data file
d_file = open('d_{}.csv'.format(subj_info[0]), 'w')

# open a window, add the FULLSCREEN flag for better timing precision
win = display.set_mode((1024,768), HWSURFACE|DOUBLEBUF)

# randomly shuffle the trial list and test them one by one
random.shuffle(trials)
for pars in trials:
    run_trial(pars, subj_info, d_file)

# close the data files and quit the program
d_file.close()
pygame.quit()
sys.exit()
