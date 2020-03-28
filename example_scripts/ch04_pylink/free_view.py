# Filename: free_view.py

import pylink
import pygame
from pygame.locals import *

# window dimension
scn_w, scn_h = (1920, 1080)

# images and correct keys for all trials
t_pars = [['lake.png', 'c'],
          ['lake_blur.png', 'b'],
          ['train.png', 'c'],
          ['train_blur.png', 'b']]

# Step 1: connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Step 2: open a Pygame window first; then call openGraphics()
# to let Pylink use the Pygame window for calibration
pygame.display.set_mode((scn_w, scn_h), DOUBLEBUF|FULLSCREEN)
pylink.openGraphics()

# Step 3: set some tracking parameters, e.g., sampling rate to 1000 Hz
# put the tracker in offline mode before we change its parameters
tk.setOfflineMode()
# give the tracker an extra 100 ms to switch operation mode
pylink.msecDelay(100)

# set the sampling rate to 1000 Hz
tk.sendCommand("sample_rate 1000")

# Send screen resolution to the tracker
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scn_w-1, scn_h-1))

# request the tracker to perform a standard 9-point calibration
tk.sendCommand("calibration_type = HV9")

#calibrate the central 80% of the screen
tk.sendCommand('calibration_area_proportion 0.8 0.8')
tk.sendCommand('validation_area_proportion 0.8 0.8')

# Step 4: open EDF data file
tk.openDataFile('freeview.edf')
# optional file header to identify the experimental task
tk.sendCommand("add_file_preamble_text 'Free Viewing'") 

# Step 5: start calibration and switch to the camera setup screen
tk.doTrackerSetup() 

# run through all four trials
for t in t_pars:
    
    # unpacking the picture and correct response key
    pic_name, cor_key = t

    # load the picture
    img = pygame.image.load('images/' + pic_name).convert()

    # record_status_message : show some info on the Host PC
    tk.sendCommand("record_status_message 'Current Picture: %s'"% pic_name)
    
    # drift check; parameters: x, y, draw_target, allow_setup
    # draw_target (1-default, 0-user draw the target then call this function)
    # allow_setup (1-allow pressing ESCAPE to recalibrate, 0-not allowed) 
    try:
        err = tk.doDriftCorrect(int(scn_w/2), int(scn_h/2), 1, 1)
    except:
        tk.doTrackerSetup()

    # start recording
    # parameters: event_in_file, sample_in_file,
    # event_over_link, sample_over_link (1-yes, 0-no)
    tk.startRecording(1,1,1,1)
    # wait for 100 ms to cache some samples
    pylink.msecDelay(100)  
    
    # present the image
    surf = pygame.display.get_surface()
    surf.blit(img, (0,0))
    pygame.display.flip()

    # log a message to mark image onset
    tk.sendMessage('Image_onset')
    
    # get key response in a while loop
    pygame.event.clear() # clear all cached events
    got_key = False
    while not got_key:
        for ev in pygame.event.get():
            if ev.type == KEYDOWN:
                if ev.key in [K_c, K_b]:
                    got_key = True
    
    # stop recording
    tk.stopRecording()
    pylink.pumpDelay(50)

# Step 6: close the EDF data file and download it
tk.closeDataFile()
tk.receiveDataFile('freeview.edf', 'freeview.edf')

# Step 7: close the link to the tracker
tk.close()

# quit pygame
pygame.quit()
