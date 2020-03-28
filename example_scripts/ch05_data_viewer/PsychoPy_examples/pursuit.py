# Filename: pursuit.py
import pylink, os, random
from psychopy import visual, core, event, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from math import sin, pi

# SETP 1: connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# STEP 2: Open an EDF data file on the Host
tk.openDataFile('pursuit.edf')
# add personalized data file header (preamble text)
tk.sendCommand("add_file_preamble_text 'Psychopy pursuit demo'")

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

# choose a calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical)
tk.sendCommand("calibration_type = HV9")

# STEP 5: prepare the pursuit target, the clock and the movement parameters
target = visual.GratingStim(win, tex=None, mask='circle', size=25)
pursuitClock = core.Clock()

# paramters for the Sinusoidal movement pattern 
# [amp_x, amp_y, phase_x, phase_y, freq_x, freq_y]
mov_pars = [[300, 300, pi*3/2, pi*2, 1.0, 1.0],
            [300, 300, pi*3/2, pi, 1.0, 1.0]]

# Step 6: show some instructions and calibrate the tracker
msg = visual.TextStim(win, text = 'Press Enter twice to calibrate the tracker', color = 'white', units = 'pix')
msg.draw()
win.flip()
event.waitKeys()

# calibrate the tracker
tk.doTrackerSetup()

# SETP 7: Run through a couple of trials
# here we define a function to group the code that will executed on each trial
def runTrial(trial_duration, movement_pars):
    """ trial_duration: the duration of the pursuit movement
        movement_pars: [ amp_x, amp_y, phase_x, phase_y, freq_x, freq_y]
        The Sinusoidal movement pattern is determined by the following equation
        y(t) = amplitude * sin(frequency * t + phase)
        for a circular or elliptical movements, the phase in x and y directions
        should be pi/2 (direction matters) """
    
    # parse the movement pattern parameters
    amp_x, amp_y, phase_x, phase_y, freq_x, freq_y = movement_pars
    
    # take the tracker offline
    tk.setOfflineMode()
    pylink.msecDelay(50)
    
    # send the standard "TRIALID" message to mark the start of a trial
    tk.sendMessage("TRIALID")

    # record_status_message : show some info on the Host PC
    tk.sendCommand("record_status_message 'Pursuit demo'")
    
    # drift check/correction, params, x, y, draw_target, allow_setup
    try:
        tk.doDriftCorrect(int(scnWidth/2-amp_x), int(scnHeight/2), 1, 1)
    except:
        tk.doTrackerSetup()

    # start recording
    # params: sample_in_file, event_in_file, sampe_over_link, event_over_link (1-yes, 0-no)
    tk.startRecording(1, 1, 1, 1)
    # wait for 50 ms to cache some samples
    pylink.msecDelay(50)
    
    # movement starts here
    win.flip()
    pursuitClock.reset()
    
    # send a message to mark movement onset
    tk.sendMessage('Movement_onset')
    while True:
        time_elapsed = pursuitClock.getTime()
        if time_elapsed >= trial_duration:
            break
        else:
            tar_x = amp_x*sin(freq_x * time_elapsed + phase_x)
            tar_y = amp_y*sin(freq_y * time_elapsed + phase_y)
            target.pos = (tar_x, tar_y)
            target.draw()
            win.flip()
            tk.sendMessage('!V TARGET_POS target %d, %d 1 0' % (tar_x + int(scnWidth/2), int(scnHeight/2)-tar_y))

    # send a message to mark movement offset
    tk.sendMessage('Movement_offset')
    # clear the subject display
    win.color=[0,0,0]
    win.flip()

    # stop recording
    tk.stopRecording() 

    # send over the standard 'TRIAL_RESULT' message to mark the end of trial
    tk.sendMessage('TRIAL_RESULT')
    pylink.pumpDelay(50)

# run a block of 2 trials, in random order
testList = mov_pars[:] 
random.shuffle(testList)
for trial in testList: 
    runTrial(10.0, trial)

# Step 8: close the EDF data file and put the tracker in idle mode
tk.closeDataFile()
tk.setOfflineMode()
pylink.pumpDelay(100)

# Step 9: copy EDF file to Display PC and put it in local folder ('edfData')
edfTransfer = visual.TextStim(win, text='EDF data is transfering from EyeLink Host PC ...', color='white')
edfTransfer.draw()
win.flip()

if not os.path.exists('edfData'): 
    os.mkdir('edfData')
tk.receiveDataFile('pursuit.edf', 'edfData/pursuit.edf')

# Step 10: close the connection to tracker, close graphics
tk.close()
core.quit()
