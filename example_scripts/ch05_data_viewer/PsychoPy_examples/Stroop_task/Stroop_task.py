#!/usr/bin/env python3
#
# Filename: Stroop_task.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# A Stroop task implemented in PsychoPy

import pylink
import os
import random
from psychopy import visual, core, event, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

# Monitor resolution
SCN_W, SCN_H = (1280, 800)

# Step 1: Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Step 2: Open an EDF data file on the Host
tk.openDataFile('stroop.edf')
# Add preamble text (file header)
tk.sendCommand("add_file_preamble_text 'Stroop task demo'")

# Step 3: Set up tracking parameters
#
# Put the tracker in idle mode before we change its parameters
tk.setOfflineMode()

# Sample rate, 250, 500, 1000, or 2000 (depending on the tracker models, 
# not all sample rate options are supported)
tk.sendCommand('sample_rate 500')

# Pass screen resolution  to the tracker
tk.sendCommand(f"screen_pixel_coords = 0 0 {SCN_W-1} {SCN_H-1}")

# Send a DISPLAY_COORDS message so Data Viewer knows the correct screen size
tk.sendMessage(f"DISPLAY_COORDS = 0 0 {SCN_W-1} {SCN_H-1}")

# Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical)
tk.sendCommand("calibration_type = HV9")

# Step 4: # open a window for graphics and calibration
#
# Create a monitor object to store monitor information
customMon = monitors.Monitor('demoMon', width=35, distance=65)

# Open a PsychoPy window
win = visual.Window((SCN_W, SCN_H), fullscr=False,
                    monitor=customMon, units='pix')

# Request Pylink to use the PsychoPy window for calibration
graphics = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(graphics)

# Step 5: calibrate the tracker, and run through all the trials
calib_prompt = "Press LEFT to RED\nRIGHT to BLEU\n\n ENTER to calibrate"
calib_msg = visual.TextStim(win, text=calib_prompt, color='white')
calib_msg.draw()
win.flip()

# Calibrate the tracker
tk.doTrackerSetup()

# Step 6: Run through all the trials
#
# Specify all possible experimental trials in a list; the columns are
# 'text', 'text_color', 'correct_answer' and "congruency"
my_trials = [
    ['red',   'red',  'left',  'cong'],
    ['red',   'blue', 'right', 'incg'],
    ['blue',  'blue', 'right', 'cong'],
    ['blue',  'red',  'left',  'incg']
    ]


# For convenience, define a run_trial function to group
# the lines of code repeatedly executed in each trial
def run_trial(params):
    """ Run a single trial

    params: a list containing tiral parameters, e.g.,
            ['red',   'red',   'left',  'cong']"""

    # Unpacking the parameters
    text, text_color, correct_answer, congruency = params

    # Prepare the stimuli
    word = visual.TextStim(win=win, text=text, font='Arial',
                           height=100.0, color=text_color)

    # Take the tracker offline
    tk.setOfflineMode()

    # Send a "TRIALID" message to mark the start of a trial
    tk.sendMessage(f"TRIALID {text} {text_color} {congruency}")

    # Record_status_message : show some info on the Host PC
    msg = f"record_status_message 'Congruency-{congruency}'"
    tk.sendCommand(msg)

    # Drift check/correction, params, x, y, draw_target, allow_setup
    tk.doDriftCorrect(int(SCN_W/2), int(SCN_H/2), 1, 1)

    # Put the tracker in idle mode before we start recording
    tk.setOfflineMode()
    
    # Start recording
    # params: file_sample, file_event, link_sampe, link_event (1-yes, 0-no)
    tk.startRecording(1, 1, 1, 1)

    # Wait for 100 ms to cache some samples
    pylink.msecDelay(100)

    # Draw the target word on the screen
    word.draw()
    win.flip()
    # Record the onset time of the stimuli
    tar_onset = core.getTime()
    # Send a message to mark the onset of visual stimuli
    tk.sendMessage("stim_onset")

    # Save a screenshot to use as background graphics in Data Viewer
    if not os.path.exists('screenshots'):
        os.mkdir('screenshots')
    screenshot = f'screenshots/cond_{text}_{text_color}.jpg'
    win.getMovieFrame()
    win.saveMovieFrames(screenshot)

    # The command we used to take screenshots takes time to return
    # we need to provide a "time offset" in the IMGLOAD message, so
    # Data Viewer knows the correct onset time of the screen
    msg_offset = int((core.getTime() - tar_onset) * 1000)
    # Send an IMGLOAD message to let DV know which screenshot to load
    scn_shot = '../' + screenshot
    tk.sendMessage(f'{msg_offset} !V IMGLOAD FILL {scn_shot}')

    # Clear bufferred events (in PsychoPy), then wait for key presses
    event.clearEvents(eventType='keyboard')
    gotKey = False
    key_pressed, RT, ACC = ['None', 'None', 'None']
    while not gotKey:
        keyp = event.getKeys(['left', 'right', 'escape'])
        if len(keyp) > 0:
            key_pressed = keyp[0]  # which key was pressed
            RT = core.getTime() - tar_onset  # response time
            # correct=1, incorrect=0
            ACC = int(key_pressed == correct_answer)

            # Send a message mark the key response
            tk.sendMessage(f"Key_resp {key_pressed}")
            gotKey = True

    # Clear the window at the end of a trials
    win.color = (0, 0, 0)
    win.flip()

    # Stop recording
    tk.stopRecording()

    # Send trial variables to record in the EDF data file
    tk.sendMessage(f"!V TRIAL_VAR word {text}")
    tk.sendMessage(f"!V TRIAL_VAR color {text_color}")
    tk.sendMessage(f"!V TRIAL_VAR congruency {congruency}")
    pylink.pumpDelay(2)  # give the link a break
    tk.sendMessage(f"!V TRIAL_VAR key_pressed {key_pressed}")
    tk.sendMessage(f"!V TRIAL_VAR RT {round(RT * 1000)}")
    tk.sendMessage(f"!V TRIAL_VAR ACC {ACC}")

    # Send a 'TRIAL_RESULT' message to mark the end of trial
    tk.sendMessage(f"TRIAL_RESULT {ACC}")

# Run a block of 8 trials, in random order
trials_to_test = my_trials[:]*2
random.shuffle(trials_to_test)
for trial in trials_to_test:
    run_trial(trial)

# Step 7: Close the EDF data file
tk.setOfflineMode() # Put tracker in offline mode
pylink.pumpDelay(100)  # wait for 100 ms
tk.closeDataFile()

# Step 8: Downlad EDF file to a local folder ('edfData')
msg = 'Downloading EDF file from the EyeLink Host PC ...'
edf = visual.TextStim(win, text=msg, color='white')
edf.draw()
win.flip()

if not os.path.exists('edfData'):
    os.mkdir('edfData')
tk.receiveDataFile('stroop.edf', 'edfData/stroop_demo.edf')

# Step 9: Close the connection to tracker, close graphics
tk.close()
win.close()
core.quit()
