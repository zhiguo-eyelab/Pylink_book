#!/usr/bin/env python3
#
# Filename: gaze_trace_plot.py
# Author: Zhiguo Wang
# Date: 4/28/2021
#
# Description:
# Extract the samples from an ASC file, then plot a gaze trace plot.

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Convert EDFs to ASC files with the edf2asc command-line tool
# If you run this script from IDLE on macOS, be sure to launch IDLE
# from the command-line (e.g., enter "idle3.6" in the terminal)
# 
# Options for the command line “edf2asc” converter
#     -r, output right-eye data only
#     -y, overwrite ASC file if exists
cmd = 'edf2asc -r -y freeview/freeview.edf'
status = os.system(cmd)

# Open the converted ASC file
asc = open(os.path.join('freeview', 'freeview.asc'))

new_trial = False
trial_DFs = {}  # samples from all trials in a tuple
trial = 0
for line in asc:
    # Extract numerical values from the data line
    values = [float(x) for x in re.findall(r'-?\d+\.?\d*', line)]

    # Look for the message marking image onset
    if re.search('image_onset', line):
        new_trial = True
        trial += 1
        print(f'processing trial # {trial}...')

        # Store samples in lists (timestamp, x, y, pupil size)
        tmp_DF = []

    # A sample data line always starts with a numerical literal
    if new_trial and re.search('^\d', line):
        # 80855874	 1506.4	  269.0	  729.0	...
        # 80855875	   .	   .	    0.0	...
        if len(values) == 4:  # normal sample line
            tmp_DF.append(values)
        else:  # sample line with missing values (e.g., tracking loss)
            tmp_DF.append([values[0], np.nan, np.nan, np.nan])

    if re.search('image_offset', line):  # message marking image offset
        # Put samples in a pandas data frame and store it in trial_DFs
        colname = ['timestamp', 'gaze_x', 'gaze_y', 'pupil']
        trial_DFs[trial] = pd.DataFrame(tmp_DF, columns=colname)
        new_trial = False

# close the ASC file
asc.close()

# Plot the gaze trace and pupil size data from trial # 1
trial_DFs[1].plot(y=['gaze_x', 'gaze_y', 'pupil'])
plt.show()
