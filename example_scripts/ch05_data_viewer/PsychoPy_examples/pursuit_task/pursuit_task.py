#!/usr/bin/env python3
#
# Filename: pursuit_task.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# A simple smooth pursuit task implemented in PsychoPy

import pylink
import os
import random
from psychopy import visual, core, event, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from math import sin, pi

# Monitor resolution
SCN_W, SCN_H = (1280, 800)

# Step 1: Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Step 2: Open an EDF data file on the Host
tk.openDataFile('pursuit.edf')
# Add preamble text (file header)
tk.sendCommand("add_file_preamble_text 'Smooth pursuit demo'")

# Step 3: Setup Host parameters
# put the tracker in idle mode before we change its parameters
tk.setOfflineMode()
pylink.msecDelay(50)

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

# Step 5: prepare the pursuit target, the clock and the movement parameters
target = visual.GratingStim(win, tex=None, mask='circle', size=25)
pursuitClock = core.Clock()

# Parameters for the Sinusoidal movement pattern
# [amp_x, amp_y, phase_x, phase_y, angular_freq_x, angular_freq_y]
mov_pars = [
    [300, 300, pi*3/2, 0, 1/8.0, 1/8.0],
    [300, 300, pi/2, 0, /8.0, 1/8.0]
    ]

# Step 6: calibrate the tracker
calib_prompt = 'Press Enter twice to calibrate the tracker'
calib_msg = visual.TextStim(win, text=calib_prompt, color='white', units='pix')
calib_msg.draw()
win.flip()

# Calibrate the tracker
tk.doTrackerSetup()


# Step 7: Run through a couple of trials
# define a function to group the code that will executed on each trial
def run_trial(trial_duration, movement_pars):
    """ Run a smooth pursuit trial

    trial_duration: the duration of the pursuit movement
    movement_pars: [amp_x, amp_y, phase_x, phase_y, freq_x, freq_y]
    The following equation defines a sinusoidal movement pattern
    y(t) = amplitude * sin(2 * pi * frequency * t + phase)
    for circular or elliptical movements, the phase in x and y directions
    should be pi/2 (direction matters)."""

    # Parse the movement pattern parameters
    amp_x, amp_y, phase_x, phase_y, freq_x, freq_y = movement_pars

    # Take the tracker offline
    tk.setOfflineMode()

    # Send the standard "TRIALID" message to mark the start of a trial
    tk.sendMessage("TRIALID")

    # Record_status_message : show some info on the Host PC
    tk.sendCommand("record_status_message 'Pursuit demo'")

    # Drift check/correction, params, x, y, draw_target, allow_setup
    tar_x = amp_x*sin(phase_x)
    tar_y = amp_y*sin(phase_y)
    target.pos = (tar_x, tar_y)
    target.draw()
    win.flip()
    tk.doDriftCorrect(int(tar_x + SCN_W/2.0), int(SCN_H/2.0 - tar_y), 0, 1)

    # Put the tracker in idle mode before we start recording
    tk.setOfflineMode()
    
    # Start recording
    # params: file_sample, file_event, link_sampe, link_event (1-yes, 0-no)
    tk.startRecording(1, 1, 1, 1)

    # Wait for 100 ms to cache some samples
    pylink.msecDelay(100)

    # Send a message to mark movement onset
    frame = 0
    while True:
        target.pos = (tar_x, tar_y)
        target.draw()
        win.flip()
        flip_time = core.getTime()
        frame += 1
        if frame == 1: 
            tk.sendMessage('Movement_onset')
            move_start = core.getTime()
        else:
            _x = int(tar_x + SCN_W/2.0)
            _y = int(SCN_H/2.0 - tar_y)
            tar_msg = f'!V TARGET_POS target {_x}, {_y} 1 0'
            tk.sendMessage(tar_msg)

        time_elapsed = flip_time - move_start

        # update the target position
        tar_x = amp_x*sin(2 * pi * freq_x * time_elapsed + phase_x)
        tar_y = amp_y*sin(2 * pi * freq_y * time_elapsed + phase_y)

        # break if the time elapsed exceeds the trial duration
        if time_elapsed > trial_duration:
            break
    
    # clear the window
    win.color = (0, 0, 0)
    win.flip()

    # Stop recording
    tk.stopRecording()

    # Send trial variables to record in the EDF data file
    tk.sendMessage(f"!V TRIAL_VAR amp_x {amp_x:.2f}")
    tk.sendMessage(f"!V TRIAL_VAR amp_y {amp_y:.2f}")
    tk.sendMessage(f"!V TRIAL_VAR phase_x {phase_x:.2f}")
    pylink.pumpDelay(2)  # give the tracker a break
    tk.sendMessage(f"!V TRIAL_VAR phase_y {phase_y:.2f}")
    tk.sendMessage(f"!V TRIAL_VAR freq_x {freq_x:.2f}")
    tk.sendMessage(f"!V TRIAL_VAR freq_y {freq_y:.2f}")
    tk.sendMessage(f"!V TRIAL_VAR duration {trial_duration:.2f}")

    # Send a 'TRIAL_RESULT' message to mark the end of the trial
    tk.sendMessage('TRIAL_RESULT')

# Run a block of 2 trials, in random order
test_list = mov_pars[:]
random.shuffle(test_list)
for trial in test_list:
    run_trial(8.0, trial)

# Step 8: Close the EDF data file and put the tracker in idle mode
tk.setOfflineMode()  # put the tracker in Offline
pylink.pumpDelay(100)  # wait for 100 ms 
tk.closeDataFile()

# Step 9: Download EDF file to a local folder ('edfData')
msg = 'Downloading EDF file from the EyeLink Host PC ...'
edf = visual.TextStim(win, text=msg, color='white')
edf.draw()
win.flip()

if not os.path.exists('edfData'):
    os.mkdir('edfData')
tk.receiveDataFile('pursuit.edf', 'edfData/pursuit_demo.edf')

# Step 10: Close the connection to tracker, close graphics
tk.close()
win.close()
core.quit()
