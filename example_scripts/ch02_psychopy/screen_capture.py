# Filename: screen_capture.py

from psychopy import visual, core

# create a window
win = visual.Window(size=[800,600], units="pix")

# get monitor frame rate
fps = win.getActualFrameRate()
print('Frame rate is: %d FPS'%fps)

# capture the screen
win.color=(0,0,0)
win.getMovieFrame()

# show the screen for 1.0 second 
win.flip()
core.wait(1.0)

# save captured screen to a JPEG
win.saveMovieFrames("gray_window.jpg") 

# quit PsychoPy 
win.close()
core.quit()