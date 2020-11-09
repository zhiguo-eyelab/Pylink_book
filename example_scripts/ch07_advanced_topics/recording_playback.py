# Filename: recording_playback.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# Playback the recording from the previous trial

import pylink
import pygame
from math import hypot

# Monitor resolution
SCN_WIDTH, SCN_HEIGHT = (800, 600)

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Send screen pixel coordinates to the tracker
tk.sendCommand('screen_pixel_coords 0 0 %d %d' % (SCN_WIDTH, SCN_HEIGHT))

# Open a Pygame window to force openGraphics() to use a
# non-fullscreen window
win = pygame.display.set_mode((SCN_WIDTH, SCN_HEIGHT))
pylink.openGraphics()

# Open an EDF data file on the Host
tk.openDataFile('playback.edf')

# Calibrate the tracker
tk.doTrackerSetup()

# Run through 3 trials
for i in range(3):
    # Start recording
    tk.startRecording(1, 1, 1, 1)

    # Show a grey fixation, a green target, and a bright distractor
    # on a black background
    win.fill((0, 0, 0))
    pygame.draw.circle(win, (128, 128, 128), (400, 300), 10)
    pygame.draw.circle(win, (0, 255, 0), (400, 100), 20)
    pygame.draw.polygon(win, (255, 255, 255),
                        [(521, 159), (541, 139), (561, 159), (541, 179)])
    pygame.display.flip()

    # Wait for a saccade towards the green target
    got_sac = False
    while not got_sac:
        dt = tk.getNextData()
        if dt == pylink.ENDSACC:
            ev_data = tk.getFloatData()
            amp_x, amp_y = ev_data.getAmplitude()
            # Break if a saccade > 2 deg is detected
            if hypot(amp_x, amp_y) > 2.0:
                got_sac = True

    tk.stopRecording()  # stop recording

    # Start playback
    tk.startPlayBack()
    # Give the Host some time to switch to the playback mode
    pylink.msecDelay(50)

    smp_pos = []
    smp_timestamp = -32768
    while True:
        # Get the newest sample
        smp = tk.getNewestSample()
        if smp is not None:
            if smp.getEye() == 0:  # left eye sample
                gaze_pos = smp.getLeftEye().getGaze()
            else:  # right eye sample
                gaze_pos = smp.getRightEye().getGaze()

            # Check if the sample is new
            if smp.getTime() > smp_timestamp:
                smp_pos.append((int(gaze_pos[0]),
                                int(gaze_pos[1])))
                smp_timestamp = smp.getTime()

                # Plot the tracjectory
                if len(smp_pos) > 1:
                    pygame.draw.lines(win, (255, 255, 255),
                                      False, smp_pos, 3)
                    pygame.display.update()

        # Exit when the playback mode ends
        if tk.getCurrentMode() == pylink.IN_IDLE_MODE:
            break

    # Keep the trajectory on the screen for a while
    pylink.pumpDelay(1500)

    # Clear up the screen
    win.fill((0, 0, 0))
    pygame.display.flip()
    pylink.pumpDelay(1000)

    # Stop playback
    tk.stopPlayBack()

# Close the EDF data file, close the link, then quit Pygame
tk.closeDataFile()
tk.close()
pygame.quit()
