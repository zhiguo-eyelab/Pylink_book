# Filename: Stroop_task.py
import pylink, os, random
from psychopy import visual, core, event, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

# SETP 1: connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# STEP 2: Open an EDF data file on the Host
tk.openDataFile('stroop.edf')
# add personalized data file header (preamble text)
tk.sendCommand("add_file_preamble_text 'Psychopy Stroop demo'")

# STEP 3: # open a window for graphics and calibration
scnWidth, scnHeight = (1280, 800)

#always create a monitor object before you run the script
customMon = monitors.Monitor('demoMon', width=35, distance=65)
customMon.setSizePix((scnWidth, scnHeight))

# open a window
win = visual.Window((scnWidth, scnHeight), fullscr=True, monitor=customMon,
                    units='pix', allowStencil=True)

# require Pylink to use custom calibration graphics--"EyeLinkCoreGraphicsPsychopy.py"
graphics = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(graphics)

# STEP 4: Setup Host parameters
# put the tracker in idle mode before we change its parameters
tk.setOfflineMode()
pylink.pumpDelay(100)

# sampling rate, 250, 500, 1000, or 2000; this command does not support EyeLInk II/I
tk.sendCommand('sample_rate 500')

# send the resolution of the monitor to the tracker
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scnWidth-1, scnHeight-1))
# save monitor resolution in EDF data file for Data Viewer to correctly load background graphics
tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

# choose a calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical), 
tk.sendCommand("calibration_type = HV9")

# STEP 5: calibrate the tracker, and run through all the trials
instructions = 'Press LEFT to RED\n\nPress RIGHT to BLEU\n\nPress ENTER to calibrate tracker'
calInstruct = visual.TextStim(win, text=instructions, color='white', )
calInstruct.draw()
win.flip()
event.waitKeys()

# calibrate the tracker
tk.doTrackerSetup()

# SETP 6: Run through all the trials
# specify all possible experimental trials
# the columns are 'text', 'textColor', 'correctAnswer' and "congruency"
myTrials = [['red',   'red',  'left',  'cong'],
            ['red',   'blue', 'right', 'incg'],
            ['blue',  'blue', 'right', 'cong'],
            ['blue',  'red',  'left',  'incg']]

# For convenience, here we define a runTrial function to group the lines
# of code executed in each trial
def runTrial(params):
    """ Run a single trial

    params: a list containing tiral parameters, e.g.,
            ['red',   'red',   'left',  'cong']"""
    
    # unpacking the parameters
    text, textColor, correctAnswer, congruency = params
    
    # prepare the stimuli
    word = visual.TextStim(win=win, text= text, font='Arial', height=100.0, color=textColor)

    # take the tracker offline
    tk.setOfflineMode()
    pylink.msecDelay(50)
    
    # send the standard "TRIALID" message to mark the start of a trial
    tk.sendMessage("TRIALID %s %s %s" % (text, textColor, congruency))

    # record_status_message : show some info on the Host PC
    tk.sendCommand("record_status_message 'word: %s, color: %s'" % (text, textColor))
    
    # drift check/correction, params, x, y, draw_target, allow_setup
    try:
        tk.doDriftCorrect(int(scnWidth/2), int(scnHeight/2), 1, 1)
    except:
        tk.doTrackerSetup()

    # start recording; params: sample_in_file, event_in_file, sampe_over_link, event_over_link (1-yes, 0-no)
    tk.startRecording(1, 1, 1, 1)
    # wait for 100 ms to cache some samples
    pylink.msecDelay(100)

    # draw the target word in the back video buffer
    word.draw()
    # save a screenshot to use as background graphics in Data Viewer
    if not os.path.exists('screenshots'): 
        os.mkdir('screenshots')
    screenshot = 'screenshots/cond_%s_%s.jpg' % (text, textColor)
    win.getMovieFrame('back')
    win.saveMovieFrames(screenshot)
    
    # flip the window to show the word, then send messages to mark stimulus onset
    win.flip()
    # record the onset time of the stimuli
    tOnset = core.getTime()
    # message to mark the onset of visual stimuli
    tk.sendMessage("stim_onset") 
    # send a Data Viewer integration message here, so DV knows which screenshot to load
    tk.sendMessage('!V IMGLOAD FILL %s' % ('..' + os.sep + screenshot))
    
    # Clear bufferred events (in PsychoPy), then wait for key presses
    event.clearEvents(eventType='keyboard')
    gotKey  = False
    keyPressed, RT, ACC = ['None', 'None', 'None']
    while not gotKey:
        keyp = event.getKeys(['left', 'right'])
        if len(keyp) > 0:
            keyPressed = keyp[0] # which key was pressed
            RT = core.getTime() - tOnset # response time
            ACC = int(keyPressed == correctAnswer) # correct=1, incorrect=0
            
            # send a message mark the key response
            tk.sendMessage("Key_resp %s" % keyPressed)
            gotKey = True

    # clear the window at the end of a trials2Test
    win.color = (0,0,0)
    win.flip()
    
    # stop recording
    tk.stopRecording() 
            
    # send trial variables to record in the EDF data file
    tk.sendMessage("!V TRIAL_VAR word %s" % (text))
    tk.sendMessage("!V TRIAL_VAR color %s" % (textColor))
    tk.sendMessage("!V TRIAL_VAR congruency %s" % (congruency))
    tk.sendMessage("!V TRIAL_VAR keyPressed %s" % (keyPressed))
    tk.sendMessage("!V TRIAL_VAR RT %d" % (RT))
    tk.sendMessage("!V TRIAL_VAR ACC %d" % (ACC))
    
    # send over the standard 'TRIAL_RESULT' message to mark the end of trial
    tk.sendMessage("TRIAL_RESULT %d" % ACC)

# run a block of of 8 trials, in random order
trials2Test = myTrials[:]*2
random.shuffle(trials2Test)
for trial in trials2Test:
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
tk.receiveDataFile('stroop.edf', 'edfData/stroop.edf')

# Step 9: close the connection to tracker, close graphics
tk.close()
core.quit()
