#!/usr/bin/env python3
#
# Filename: demo_screenshot.py
# Author: Zhiguo Wang
# Date: 2/7/2021
#
# Description:
# Get the actual frame rate, then take a screenshot

from psychopy import visual, core

# Open a window
win = visual.Window(size=[1280, 800], units="pix", fullscr=True)

# Get frame rate (frame per second)
fps = win.getActualFrameRate()
print('Frame rate is: {} FPS'.format(fps))

# Show the screen for 1.0 second
win.color = (0, 0, 0)
win.flip()
core.wait(1.0)

# Grab a screenshot and save it to a JPEG
win.getMovieFrame()
win.saveMovieFrames("gray_window.jpg")

# Close the window and quit PsychoPy
win.close()
core.quit()
