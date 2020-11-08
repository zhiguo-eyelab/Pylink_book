# Filename: minimalist_example.py

import pylink

# Step 1: Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Step 2: open an EDF data file on the EyeLink Host PC
tk.openDataFile('test.edf')

# Step 3: set some tracking parameters
tk.sendCommand("sample_rate 1000")

# Step 4: open calibration window
pylink.openGraphics()

# Step 5: calibrate the tracker, then run five trials
tk.doTrackerSetup()

for i in range(5):
    # start recording
    tk.startRecording(1,1,1,1)
    # record data for 2 seconds
    pylink.msecDelay(2000) 
    # stop recording
    tk.stopRecording()

# Step 6: close the EDF data file and download it
tk.closeDataFile()
tk.receiveDataFile('test.edf', 'test.edf')

# Step 7: close the graphics and the link to the tracker
pylink.closeGraphics()
tk.close()
