#!/usr/bin/env python3
#
# Filename: video_task.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# Play video and record eye movements in Psychopy

import pylink
import os
import random
from psychopy import visual, core, event, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy.constants import FINISHED

# Screen resolution
SCN_W, SCN_H = (1280, 800)

# SETP 1: Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Step 2: Open an EDF data file on the Host
tk.openDataFile('video.edf')
# Add preamble text (file header)
tk.sendCommand("add_file_preamble_text 'Movie playback demo'")

# Step 3: Set up tracking parameters
#
# put the tracker in idle mode before we change its parameters
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

# Step 5: Calibrate the tracker, and run through all the trials
calib_prompt = "Press ENTER to calibrate the tracker"
calib_msg = visual.TextStim(win, text=calib_prompt, color='white', )
calib_msg.draw()
win.flip()

# Calibrate the tracker
tk.doTrackerSetup()

# Step 6: Run through a couple of trials
# put the videos we would like to play in a list
trials = [
    ['t1', 'driving.mp4'],
    ['t2', 'driving.mp4']
    ]


# Here we define a helper function to group the code executed on each trial
def run_trial(pars):
    """ pars corresponds to a row in the trial list"""

    # Retrieve parameters from the trial list
    trial_num, movie_file = pars

    # Load the video to display
    mov = visual.MovieStim3(win, filename=movie_file, size=(960, 540))

    # Take the tracker offline
    tk.setOfflineMode()

    # Send the standard "TRIALID" message to mark the start of a trial
    tk.sendMessage(f"TRIALID {trial_num} {movie_file}")

    # Record_status_message : show some info on the Host PC
    msg = f"record_status_message 'Movie File: {movie_file}'"
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

    # The size of the video
    mo_width, mo_height = mov.size

    # play the video till the end
    frame_n = 0
    prev_frame_timestamp = mov.getCurrentFrameTime()
    while mov.status is not FINISHED:
        # draw a movie frame and flip the video buffer
        mov.draw()
        win.flip()

        # if a new frame is drawn, check frame timestamp and
        # send a VFRAME message
        current_frame_timestamp = mov.getCurrentFrameTime()
        if current_frame_timestamp != prev_frame_timestamp:
            frame_n += 1
            # send a message to mark the onset of each video frame
            tk.sendMessage(f'Video_Frame: {frame_n}')
            # VFRAME message: "!V VFRAME frame_num movie_pos_x,
            # movie_pos_y, path_to_movie_file"
            x = int(SCN_W/2 - mo_width/2)
            y = int(SCN_H/2 - mo_height/2)
            path_to_movie = os.path.join('..', movie_file)
            msg = f"!V VFRAME {frame_n} {x} {y} {path_to_movie}"
            tk.sendMessage(msg)
            prev_frame_timestamp = current_frame_timestamp

    # Send a message to mark video playback end
    tk.sendMessage("Video_terminates")

    # Clear the subject display
    win.color = (0, 0, 0)
    win.flip()

    # Stop recording
    tk.stopRecording()

    # Send a'TRIAL_RESULT' message to mark the end of trial
    tk.sendMessage('TRIAL_RESULT')

# Run a block of 2 trials, in random order
test_list = trials[:]
random.shuffle(test_list)
for trial in test_list:
    run_trial(trial)

# Step 7: Close the EDF data file
pylink.pumpDelay(100)  # wait for 100 ms to catch session end events
tk.closeDataFile()

# Step 8: Download EDF file to a local folder ('edfData')
msg = 'Downloading EDF file from the EyeLink Host PC ...'
edfTransfer = visual.TextStim(win, text=msg, color='white')
edfTransfer.draw()
win.flip()

if not os.path.exists('edfData'):
    os.mkdir('edfData')
tk.receiveDataFile('video.edf', 'edfData/video_demo.edf')

# Step 9: Close the connection to tracker, close graphics
tk.close()
win.close()
core.quit()
