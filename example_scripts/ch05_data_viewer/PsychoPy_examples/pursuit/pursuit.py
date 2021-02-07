#!/usr/bin/env python
#
# Filename: pursuit.py
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

# Sample rate, 250, 500, 1000, or 2000
# this command does not support EyeLInk II/I
tk.sendCommand('sample_rate 500')

# Send the resolution of the monitor to the tracker
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (SCN_W-1, SCN_H-1))

# Save monitor resolution in EDF data file,
# so Data Viewer can correctly load background graphics
tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (SCN_W-1, SCN_H-1))

# Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical)
tk.sendCommand("calibration_type = HV9")

# Step 4: # open a window for graphics and calibration
#
# Create a monitor object to store monitor information
customMon = monitors.Monitor('demoMon', width=35, distance=65)

# Open a PsychoPy window
win = visual.Window((SCN_W, SCN_H), fullscr=True,
                    monitor=customMon, units='pix')

# Request Pylink to use the PsychoPy window for calibration
graphics = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(graphics)

# Step 5: prepare the pursuit target, the clock and the movement parameters
target = visual.GratingStim(win, tex=None, mask='circle', size=25)
pursuitClock = core.Clock()

# Paramters for the Sinusoidal movement pattern
# [amp_x, amp_y, phase_x, phase_y, freq_x, freq_y]
mov_pars = [
    [300, 300, pi*3/2, 0, 1.0, 1.0],
    [300, 300, pi/2, 0, 1.0, 1.0]
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
    movement_pars: [ amp_x, amp_y, phase_x, phase_y, freq_x, freq_y]
    The Sinusoidal movement pattern is determined by the following equation
    y(t) = amplitude * sin(frequency * t + phase)
    for a circular or elliptical movements, the phase in x and y directions
    should be pi/2 (direction matters) """

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
    try:
        tk.doDriftCorrect(int(tar_x + SCN_W/2),
                          int(SCN_H/2 - tar_y), 0, 1)
    except:
        tk.doTrackerSetup()

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
            _x = int(tar_x + SCN_W/2)
            _y = int(SCN_H/2 - tar_y)
            tar_msg = '!V TARGET_POS target {}, {} 1 0'.format(_x, _y)
            tk.sendMessage(tar_msg)

        time_elapsed = flip_time - move_start

        # update the target position
        tar_x = amp_x*sin(freq_x * time_elapsed + phase_x)
        tar_y = amp_y*sin(freq_y * time_elapsed + phase_y)
        print(time_elapsed, tar_x, tar_y)
        # break if the time elapsed exceeds the trial duration
        if time_elapsed > trial_duration:
            break
    
    # clear the window
    win.color = (0, 0, 0)
    win.flip()

    # Stop recording
    tk.stopRecording()

    # Send trial variables to record in the EDF data file
    tk.sendMessage("!V TRIAL_VAR amp_x {0:.2f}".format(amp_x))
    tk.sendMessage("!V TRIAL_VAR amp_y {0:.2f}".format(amp_y))
    tk.sendMessage("!V TRIAL_VAR phase_x {0:.2f}".format(phase_x))
    tk.sendMessage("!V TRIAL_VAR phase_y {0:.2f}".format(phase_y))
    tk.sendMessage("!V TRIAL_VAR freq_x {0:.2f}".format(freq_x))
    tk.sendMessage("!V TRIAL_VAR freq_y {0:.2f}".format(freq_y))
    tk.sendMessage("!V TRIAL_VAR duration {0:.2f}".format(trial_duration))

    # Send a 'TRIAL_RESULT' message to mark the end of trial
    tk.sendMessage('TRIAL_RESULT')

# Run a block of 2 trials, in random order
test_list = mov_pars[:]
random.shuffle(test_list)
for trial in test_list:
    run_trial(6.0, trial)

# Step 9: Downlad EDF file to a local folder ('edfData')
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
