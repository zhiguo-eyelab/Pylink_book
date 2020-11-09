# Filename: broadcast_simple.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# Broadcast allows users to retrieve realtime eye movement data
# on a second computer

import pylink
listener = pylink.EyeLinkListener()

print('Wait for a primary connection to the tracker...')
link_connected = 0
while not link_connected:
    # Link status info, returns an instance of the ILinkData class
    idata = listener.getTrackerInfo()

    # Use the requestTime() and readTime() functions in pair to
    # check if the tracker is active; if so, readTime() should return
    # a non-zero value
    listener.requestTime()
    t_start = pylink.currentTime()
    while (pylink.currentTime()-t_start < 500):
        tracker_time = listener.readTime()
        if tracker_time is not 0:
            if (idata.getLinkFlags() & pylink.LINK_CONNECTED):
                print('Link Status: %s - connected' % idata.getLinkFlags())
                link_connected = pylink.LINK_CONNECTED
                break

# Request the Host PC to switch to enter the broadcast mode
listener.broadcastOpen()

# If there is a primary connection, check the current operation mode
# and save the sample data (gaze position) to file if in recording mode
smp_data = open('sample_data.csv', 'w')
mode = -1  # initial tracker operation mode
smp_t = -32768  # initial timestamp for samples
while listener.isConnected():
    # Get the current Host mode and print it out
    current_mode = listener.getTrackerMode()  
    if current_mode is not mode:
        mode = current_mode
        if current_mode == pylink.EL_SETUP_MENU_MODE:
            print('Current mode: %d - EL_SETUP_MENU_MODE' % mode)
        if current_mode == pylink.EL_CALIBRATE_MODE:
            print('Current mode: %d - EL_CALIBRATE_MODE' % mode)
        if current_mode == pylink.EL_OPTIONS_MENU_MODE:
            print('Current mode: %d - EL_OPTIONS_MENU_MODE' % mode)
        if current_mode == pylink.EL_VALIDATE_MODE:
            print('Current mode: %d - EL_VALIDATE_MODE' % mode)
        if current_mode == pylink.EL_DRIFT_CORR_MODE:
            print('Current mode: %d - EL_DRIFT_CORR_MODE' % mode)
        if current_mode == pylink.EL_RECORD_MODE:
            print('Current mode: %d - EL_RECORD_MODE' % mode)

    # Retrieve sample data if the tracker is in RECORD_MODE
    if current_mode == pylink.EL_RECORD_MODE:
        smp = listener.getNewestSample()
        if (smp is not None) and (smp.getTime() != smp_t):
            smp_t = smp.getTime()
            if smp.isRightSample():
                gaze_x, gaze_y = smp.getRightEye().getGaze()
            elif smp.isLeftSample():
                gaze_x, gaze_y = smp.getLeftEye().getGaze()
            # Write the gaze position to file
            smp_data.write('%d, %d, %d\n' % (smp_t, gaze_x, gaze_y))
