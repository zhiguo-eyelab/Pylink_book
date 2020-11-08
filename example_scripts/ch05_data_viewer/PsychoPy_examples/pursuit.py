# Filename: pursuit.py
# Author: Zhiguo Wang
# Date: 11/7/2020
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
SCN_WIDTH, SCN_HEIGHT = (1280, 800)

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
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (SCN_WIDTH-1, SCN_HEIGHT-1))

# Save monitor resolution in EDF data file,
# so Data Viewer can correctly load background graphics
tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (SCN_WIDTH-1, SCN_HEIGHT-1))

# Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical)
tk.sendCommand("calibration_type = HV9")

# Step 4: # open a window for graphics and calibration
# Always create a monitor object before you run the script
customMon = monitors.Monitor('demoMon', width=35, distance=65)
customMon.setSizePix((SCN_WIDTH, SCN_HEIGHT))

# Open a window
win = visual.Window((SCN_WIDTH, SCN_HEIGHT), fullscr=False,
                    monitor=customMon, units='pix', allowStencil=True)

# Request Pylink to use the PsychoPy window for calibration
graphics = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(graphics)

# Step 5: prepare the pursuit target, the clock and the movement parameters
target = visual.GratingStim(win, tex=None, mask='circle', size=25)
pursuitClock = core.Clock()

# Paramters for the Sinusoidal movement pattern
# [amp_x, amp_y, phase_x, phase_y, freq_x, freq_y]
mov_pars = [
    [300, 300, pi*3/2, pi*2, 1.0, 1.0],
    [300, 300, pi*3/2, pi, 1.0, 1.0]
    ]

# Step 6: show some instructions and calibrate the tracker.
calib_prompt = 'Press Enter twice to calibrate the tracker'
calib_msg = visual.TextStim(win, text=calib_prompt, color='white', units='pix')
calib_msg.draw()
win.flip()
event.waitKeys()

# Calibrate the tracker
tk.doTrackerSetup()


# Step 7: Run through a couple of trials
# here we define a function to group the code that will executed on each trial
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
    pylink.msecDelay(50)

    # Send the standard "TRIALID" message to mark the start of a trial
    tk.sendMessage("TRIALID")

    # Record_status_message : show some info on the Host PC
    tk.sendCommand("record_status_message 'Pursuit demo'")

    # Drift check/correction, params, x, y, draw_target, allow_setup
    try:
        tk.doDriftCorrect(int(SCN_WIDTH/2-amp_x), int(SCN_HEIGHT/2), 1, 1)
    except:
        tk.doTrackerSetup()

    # Start recording
    # params: sample_in_file, event_in_file,
    # sampe_over_link, event_over_link (1-yes, 0-no)
    tk.startRecording(1, 1, 1, 1)
    # Wait for 50 ms to cache some samples
    pylink.msecDelay(50)

    # Movement starts here
    win.flip()
    pursuitClock.reset()

    # Send a message to mark movement onset
    tk.sendMessage('Movement_onset')
    while True:
        time_elapsed = pursuitClock.getTime()
        if time_elapsed >= trial_duration:
            break
        else:
            tar_x = amp_x*sin(freq_x * time_elapsed + phase_x)
            tar_y = amp_y*sin(freq_y * time_elapsed + phase_y)
            target.pos = (tar_x, tar_y)
            target.draw()
            win.flip()
            tar_pos = (tar_x + int(SCN_WIDTH/2), int(SCN_HEIGHT/2)-tar_y)
            tk.sendMessage('!V TARGET_POS target %d, %d 1 0' % tar_pos)

    # Send a message to mark movement offset
    tk.sendMessage('Movement_offset')
    # clear the subject display
    win.color = (0, 0, 0)
    win.flip()

    # Stop recording
    tk.stopRecording()

    # Send trial variables to record in the EDF data file
    tk.sendMessage("!V TRIAL_VAR amp_x %.2f" % amp_x)
    tk.sendMessage("!V TRIAL_VAR amp_y %.2f" % amp_y)
    tk.sendMessage("!V TRIAL_VAR phase_x %.2f" % phase_x)
    tk.sendMessage("!V TRIAL_VAR phase_y %.2f" % phase_y)
    tk.sendMessage("!V TRIAL_VAR freq_x %.2f" % freq_x)
    tk.sendMessage("!V TRIAL_VAR freq_y %.2f" % freq_y)
    tk.sendMessage("!V TRIAL_VAR duration %.2f" % trial_duration)

    # Send a 'TRIAL_RESULT' message to mark the end of trial
    tk.sendMessage('TRIAL_RESULT')
    pylink.pumpDelay(50)

# Run a block of 2 trials, in random order
test_list = mov_pars[:]
random.shuffle(test_list)
for trial in test_list:
    run_trial(5.0, trial)

# Step 8: Close the EDF data file and put the tracker in idle mode
tk.closeDataFile()
tk.setOfflineMode()
pylink.pumpDelay(100)

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
core.quit()
