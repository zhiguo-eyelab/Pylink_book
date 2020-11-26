# Filename: demo_screenshot.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# Get the actual frame rate, then take a screenshot

from psychopy import visual, core

# Open a window
win = visual.Window(size=[800, 600], units="pix")

# Get frame rate (frame per second)
fps = win.getActualFrameRate()
print('Frame rate is: %d FPS' % fps)

# Capture the screen
win.color = (0, 0, 0)
win.getMovieFrame()

# Show the screen for 1.0 second
win.flip()
core.wait(1.0)

# Save captured screen to a JPEG
win.saveMovieFrames("gray_window.jpg")

# Quit PsychoPy
win.close()
core.quit()
