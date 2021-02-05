# Filename: free_viewing.py
# Author: Zhiguo Wang
# Date: 11/11/2020
#
# Description:
# A free-viewing task implemented in Pygame.

import os
import pylink
import pygame
from pygame.locals import *

# Screen resolution
SCN_WIDTH, SCN_HEIGHT = (1920, 1080)

# Images and the correct response keys for all trials
t_pars = [['lake.png', 'c'],
    ['lake_blur.png', 'b'],
    ['train.png', 'c'],
    ['train_blur.png', 'b']]

# Step 1: Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Step 2: open an EDF data file on the EyeLink Host PC
tk.openDataFile('freeview.edf')
# Optional file header
tk.sendCommand("add_file_preamble_text 'Free Viewing Task'")

# Step 3: Set tracking parameters, e.g., sampling rate
# Put the tracker in offline mode before we change its parameters
tk.setOfflineMode()
# Set the sampling rate to 1000 Hz
tk.sendCommand("sample_rate 1000")
# Send screen resolution to the tracker
coords = (SCN_WIDTH-1, SCN_HEIGHT-1)
tk.sendCommand("screen_pixel_coords = 0 0 {} {}".format(coords))
# Request the tracker to perform a 9-point calibration
tk.sendCommand("calibration_type = HV9")
# Calibrate the central 80% of the screen
tk.sendCommand('calibration_area_proportion 0.8 0.8')
tk.sendCommand('validation_area_proportion 0.8 0.8')

# Step 4: open a Pygame window first; call pylink.openGraphics()
# to request Pylink to use this window for calibration
pygame.display.set_mode((SCN_WIDTH, SCN_HEIGHT), DOUBLEBUF | FULLSCREEN)
pylink.openGraphics()

# Step 5: calibrate the tracker, then run through the trials
tk.doTrackerSetup()

# run through all four trials
for trial in t_pars:
    # Unpacking the picture and correct response key
    pic, cor_key = trial

    # Load the picture
    pic_path = os.path.join('images', pic)
    img = pygame.image.load(pic_path).convert()

    # Record_status_message: show some info on the Host PC
    tk.sendCommand("record_status_message 'Picture: {}'".format(pic))

    # Drift check and re-calibrate if ESCAPE is pressed
    # parameters: x, y, draw_target, allow_setup
    # draw_target (1-use default target, 0-draw the target yourself)
    # allow_setup (1-allow recalibrate, 0-not allowed)
    tk.doDriftCorrect(int(SCN_WIDTH/2), int(SCN_HEIGHT/2), 1, 1)

    # Start recording
    # parameters: file_event, file_sample, link_event, link_sample
    # event_over_link, sample_over_link (1-yes, 0-no)
    tk.startRecording(1, 1, 1, 1)
    # Wait for 100 ms to cache some samples
    pylink.msecDelay(100)

    # Present the image
    surf = pygame.display.get_surface()
    surf.blit(img, (0, 0))
    pygame.display.flip()

    # Log a message to mark image onset
    tk.sendMessage('Image_onset')

    # Wait for a key response
    pygame.event.clear()  # clear all cached events
    got_key = False
    while not got_key:
        for ev in pygame.event.get():
            if ev.type == KEYDOWN and ev.key in [K_c, K_b]:
                tk.sendMessage('Keypress {}'.format(ev.key))
                got_key = True

    # stop recording
    tk.stopRecording()

# Step 6: close the EDF data file and download it
tk.closeDataFile()
tk.receiveDataFile('freeview.edf', 'freeview.edf')

# Step 7: close the link to the tracker and quit Pygame
tk.close()
pygame.quit()
