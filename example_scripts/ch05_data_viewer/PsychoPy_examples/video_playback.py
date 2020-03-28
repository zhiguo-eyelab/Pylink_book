# Filename: video_playback.py
import pylink, os, random
from psychopy import visual, core, event, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy.constants import STOPPED, PLAYING

# SETP 1: connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# STEP 2: Open an EDF data file on the Host
tk.openDataFile('video.edf')
# add personalized data file header (preamble text)
tk.sendCommand("add_file_preamble_text 'Psychopy video demo'")

# STEP 3: # open a window for graphics and calibration
scnWidth, scnHeight = (1280, 800)

#always create a monitor object before you run the script
customMon = monitors.Monitor('demoMon', width=35, distance=65)
customMon.setSizePix((scnWidth, scnHeight))

# open a window
win = visual.Window((scnWidth, scnHeight), fullscr=True, monitor=customMon, units='pix', allowStencil=True)

# require Pylink to use custom calibration graphics--"EyeLinkCoreGraphicsPsychopy.py"
graphics = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(graphics)

# STEP 4: Setup Host parameters
# put the tracker in idle mode before we change its parameters
tk.setOfflineMode()
pylink.pumpDelay(50)

# sampling rate, 250, 500, 1000, or 2000; this command does not support EyeLInk II/I
tk.sendCommand('sample_rate 500')

# send the resolution of the monitor to the tracker
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scnWidth-1, scnHeight-1))
# save monitor resolution in EDF data file for Data Viewer to correctly load background graphics
tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

# choose a calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical), 
tk.sendCommand("calibration_type = HV9")

# Step 5: show some instructions and calibrate the tracker.
msg = visual.TextStim(win, text = 'Press Enter twice to calibrate the tracker', color = 'white', units = 'pix')
msg.draw()
win.flip()
event.waitKeys()

# calibrate the tracker
tk.doTrackerSetup()

# SETP 6: Run through a couple of trials
# put the videos we would like to play in a list
trials = [['t1', 'Seoul.mp4'],
          ['t2', 'Seoul.mp4']]

# here we define a helper function to group the code executed on each trial
def runTrial(pars):
    """ pars corresponds to a row in the trial list"""

    # retrieve paramters from the trial list
    trial_num, movieFile = pars 

    # load the video to display
    mov = visual.MovieStim3(win, filename=movieFile, size=(960, 540))
    
    # take the tracker offline
    tk.setOfflineMode()
    pylink.msecDelay(50)
    
    # send the standard "TRIALID" message to mark the start of a trial
    tk.sendMessage("TRIALID %s %s" % (trial_num, movieFile))

    # record_status_message : show some info on the Host PC
    tk.sendCommand("record_status_message 'Trial: %s, movie File: %s'" % (trial_num, movieFile))
    
    # drift check/correction, params, x, y, draw_target, allow_setup
    try:
        tk.doDriftCorrect(int(scnWidth/2), int(scnHeight/2), 1, 1)
    except:
        tk.doTrackerSetup()

    # start recording;
    # params: sample_in_file, event_in_file, sampe_over_link, event_over_link (1-yes, 0-no)
    tk.startRecording(1, 1, 1, 1)
    # wait for 50 ms to cache some samples
    pylink.msecDelay(50)

    # the size of the video
    movWidth, movHeight = mov.size
    # position the movie at the center of the screen
    movX = int(scnWidth/2-movWidth/2)
    movY = int(scnHeight/2-movHeight/2)

    # play the video till the end
    frameNum = 0    
    previousFrameTimeStamp = mov.getCurrentFrameTime()
    while mov.status is not STOPPED:
        # draw a movie frame and flip the video buffer
        mov.draw()
        win.flip()

        # if a new frame is drawn, check frame timestamp and send a VFRAME message
        currentFrameTimeStamp = mov.getCurrentFrameTime()
        if currentFrameTimeStamp != previousFrameTimeStamp:
            frameNum += 1
            # store a message in the EDF to mark the onset of each video frame
            tk.sendMessage('Video_Frame: %d' % frameNum)
            # VFRAME message: "!V VFRAME frame_num movie_pos_x, movie_pos_y, path_to_file" 
            tk.sendMessage("!V VFRAME %d %d %d %s" % (frameNum, movX, movY, "../" + movieFile))
            previousFrameTimeStamp = currentFrameTimeStamp

    tk.sendMessage("Video_terminates")
    # clear the subject display
    win.color=[0,0,0]
    win.flip()

    # stop recording
    tk.stopRecording() 

    # send over the standard 'TRIAL_RESULT' message to mark the end of trial
    tk.sendMessage('TRIAL_RESULT')
    pylink.pumpDelay(50)

# run a block of 2 trials, in random order
testList = trials[:] 
random.shuffle(testList)
for trial in testList: 
    runTrial(trial)

# Step 7: close the EDF data file and put the tracker in idle mode
tk.closeDataFile()
tk.setOfflineMode()
pylink.pumpDelay(100)

# Step 8: copy EDF file to Display PC and put it in local folder ('edfData')
edfTransfer = visual.TextStim(win, text='EDF data is transfering from EyeLink Host PC ...', color='white')
edfTransfer.draw()
win.flip()

if not os.path.exists('edfData'): 
    os.mkdir('edfData')
tk.receiveDataFile('video.edf', 'edfData/video.edf')

# Step 9: close the connection to tracker, close graphics
tk.close()
core.quit()
