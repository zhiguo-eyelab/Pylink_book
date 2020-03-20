# Filename: demo.py

# This script shows how to request Pylink to use a custom calibration 
# graphics library -- EyeLinkCoreGraphcicPsychoPy

import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors 

# connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# open a PsychoPy window
scnWidth, scnHeight = (1024, 768)
# be sure to explicitly set monitor parameters
mon = monitors.Monitor('myMac15', width=53.0, distance=70.0)
mon.setSizePix((scnWidth, scnHeight))
# open a window
win = visual.Window((scnWidth, scnHeight), fullscr=False, monitor=mon, units='pix')

# instantiate a custom CoreGraphics environment in PsychoPy
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
# to use a dynamic spiral as the calibration target; otherwise, calTarget could be
# a "circle", a "picture", or a "movie" clip. To use a picture or movie clip as the
# calibration target, you need to provide movieTargetFile or pictureTargetFile
genv.calTarget = 'spiral'
# provide a movie clip if genv.calTarget = 'movie'
#genv.movieTargetFile = 'starjumps100.avi'
genv.targetSize = 32

# open the calibration window
pylink.openGraphicsEx(genv)

# set up the camera and calibrate the tracker
tk.doTrackerSetup()

# close the connection and close the PsychoPy window
tk.close()
win.close()
core.quit()
