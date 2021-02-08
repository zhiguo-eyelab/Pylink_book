#!/usr/bin/env python3
#
# Filename: free_viewing.py
# Author: Zhiguo Wang
# Date: 2/7/2020
#
# Description:
# A free-viewing task implemented in Pygame.

import os
import pylink
import pygame
from pygame.locals import *

# Screen resolution
SCN_W, SCN_H = (1280, 800)

# Step 1: Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Step 2: open an EDF data file on the EyeLink Host PC
tk.openDataFile('freeview.edf')
# Optional file header
tk.sendCommand("add_file_preamble_text 'Free Viewing Task'")

# Step 3: Set tracking parameters, e.g., sampling rate
#
# Put the tracker in offline mode before we change its parameters
tk.setOfflineMode()

# Set the sampling rate to 1000 Hz
tk.sendCommand("sample_rate 1000")

# Send screen resolution to the tracker
tk.sendCommand(f"screen_pixel_coords = 0 0 {SCN_W-1} {SCN_H-1}")

# Record a DISPLAY_SCREEN message to let Data Viewer know the
# correct screen resolution to use when visualizing the data
tk.sendMessage(f'DISPLAY_SCREEN 0 0 {SCN_W - 1} {SCN_H - 1}')

# Request the tracker to perform a 9-point calibration
tk.sendCommand("calibration_type = HV9")

# Calibrate the central 80% of the screen
tk.sendCommand('calibration_area_proportion 0.8 0.8')
tk.sendCommand('validation_area_proportion 0.8 0.8')

# Step 4: open a Pygame window; then, call pylink.openGraphics()
# to request Pylink to use this window for calibration
pygame.display.set_mode((SCN_W, SCN_H), DOUBLEBUF | FULLSCREEN)
pylink.openGraphics()

# Step 5: calibrate the tracker, then run through the trials
tk.doTrackerSetup()

# Images and the correct response keys for all trials
t_pars = [
    ['lake.png', 'c'],
    ['lake_blur.png', 'b'],
    ['train.png', 'c'],
    ['train_blur.png', 'b']
    ]

# Define a function to group the lines of code that will be executed
# in each trial
def run_trial(params):
    ''' Run a trial
    params: a list containing the picture to present and the correct
    keypress, e.g., ['lake.png', 'c'] '''
    
    # Unpacking the picture and correct keypress
    pic, cor_key = params

    # Load the picture, scale the image to fill up the screen
    pic_path = os.path.join('images', pic)
    img = pygame.image.load(pic_path).convert()
    img = pygame.transform.scale(img, (SCN_W, SCN_H))

    # clear the host screen before we draw a backdrop on the Host PC
    el_tracker.sendCommand('clear_screen 0')

    # draw the backdrop with the bitmapBackdrop() command, see chapter 7
    # parameters: width, height, pixel, crop_x, crop_y,
    #             crop_width, crop_height, x, y on the Host, drawing options
    pixels = [[img.get_at((i, j))[0:3] for i in range(scn_width)]
              for j in range(scn_height)]
    el_tracker.bitmapBackdrop(SCN_W, SCN_H, pixels, 0, 0, SCN_W, SCN_H,
                              0, 0, pylink.BX_MAXCONTRAST)

    # Record_status_message: show some info on the Host PC
    tk.sendCommand("record_status_message 'Picture: {pic}'")

    # Drift-check; re-calibrate if ESCAPE is pressed
    # parameters: x, y, draw_target, allow_setup
    tk.doDriftCorrect(int(SCN_W/2), int(SCN_H/2), 1, 1)

    # Start recording
    # parameters: file_event, file_sample, link_event, link_sample
    tk.startRecording(1, 1, 1, 1)
    # Wait for 100 ms to cache some samples
    pylink.msecDelay(100)

    # Present the image
    surf = pygame.display.get_surface()
    surf.blit(img, (0, 0))
    pygame.display.flip()

    # Log a message to mark image onset
    tk.sendMessage('Image_onset')

    # Log a '!V IMGLOAD' message to the EDF data file, so Data Viewer
    # knows where to find the image when visualizing the gaze data
    img_path = os.path.join('images', pic)
    tk.sendMessage(f'!V IMGLOAD FILL {img_path}')

    # Wait for a key response
    pygame.event.clear()  # clear all cached events
    got_key = False
    while not got_key:
        for ev in pygame.event.get():
            if ev.type == KEYDOWN and ev.key in [K_c, K_b]:
                tk.sendMessage(f'Keypress {ev.key}')
                got_key = True

    # stop recording
    tk.stopRecording()

# Run through all four trials in a random order
random.shuffle(t_pars)
for trial in t_pars:
    run_trial(trial)
    
# Step 6: close the EDF data file and download it
tk.closeDataFile()
tk.receiveDataFile('freeview.edf', 'freeview.edf')

# Step 7: close the link to the tracker and quit Pygame
tk.close()
pygame.quit()
