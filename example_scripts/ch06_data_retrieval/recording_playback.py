# Filename: recording_playback.py

import pylink
import pygame
from math import hypot

# connect to the tracker
tk = pylink.EyeLink()

# send screen coordinates to the tracker
tk.sendCommand('screen_pixel_coords 0 0 800 600')

# open a Pygame window to force openGraphics() to use a non-fullscreen window
win = pygame.display.set_mode((800, 600)) 
pylink.openGraphics()

# open a data file, so we can playback the recorded data
tk.openDataFile('playback.edf')

# calibrate the tracker, one can run in mouse simulation mode
tk.doTrackerSetup()

# run 5 trials of a simple visual distractor task
for i in range(5):

    # start recording
    tk.startRecording(1,1,1,1)
    
    # a grey fixation, a green target, and a bright distractor on a black background
    win.fill((0,0,0))
    pygame.draw.circle(win, (128,128,128), (400,300), 10)
    pygame.draw.circle(win, (0,255,0), (400,100), 20)
    pygame.draw.polygon(win, (255,255,255), [(521,159),(541,139),(561,159),(541,179)])
    pygame.display.flip()    

    # wait for a saccadic response
    got_SAC = False
    while not got_SAC:
        dt = tk.getNextData()
        if dt is not None:
            ev_data = tk.getFloatData()
            if dt == pylink.ENDSACC:
                amp_x, amp_y =  ev_data.getAmplitude()
                # jump out of the loop if a saccade >2 deg is detected
                if hypot(amp_x, amp_y) > 2.0:
                    got_SAC = True

    tk.stopRecording() # stop recording

    #start playback and draw the saccade trajectory
    tk.startPlayBack()
    pylink.pumpDelay(50) # wait for 50 ms so the Host can switch to playback mode
    smp_pos = []
    smp_timestamp = -32768
    while True:
        smp = tk.getNewestSample()
        if smp is not None:
            if smp.getEye() == 0:
                gaze_pos = smp.getLeftEye().getGaze()
            else:
                gaze_pos = smp.getRightEye().getGaze()
            if smp.getTime() > smp_timestamp:
                smp_pos = smp_pos + [(int(gaze_pos[0]), int(gaze_pos[1]))]
                smp_timestamp = smp.getTime()

                # plot the tracjectory
                if len(smp_pos) > 1:
                    pygame.draw.lines(win, (255,255,255), False, smp_pos, 3)
                    pygame.display.update()
                    
        if tk.getCurrentMode() == pylink.IN_IDLE_MODE:
            break

    # keep the trajectory on screen for a while
    pylink.pumpDelay(1500)
    # clear up the screen
    win.fill((0,0,0)) 
    pygame.display.flip()
    pylink.pumpDelay(1000)

    # stop playback            
    tk.stopPlayBack()
    
tk.closeDataFile()
tk.close()
pygame.quit()
    
