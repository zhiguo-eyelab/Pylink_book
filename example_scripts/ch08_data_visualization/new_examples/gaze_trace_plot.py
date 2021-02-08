#!/usr/bin/env python3
#
# Filename: gaze_trace_plot.py
# Author: Zhiguo Wang
# Date: 2/8/2021
#
# Description:
# Extract sample data from the ASC file, then plot a gaze trace plot.

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Open the converted ASC file
asc = open(os.path.join('freeview', 'freeview.asc'))

scn_w, scn_h = [-32768, -32768]
trial_start = False
trial_DFs = {}  # data frames from all trials in a tuple
trial_number = 0
for line in asc:
    # Extract numerical values from the data line
    tmp_data = [float(x) for x in re.findall(r'-?\d+\.?\d*', line)]

    # Message marking image onset
    if re.search('image_onset', line):
        trial_start = True
        trial_number += 1
        # Store the samples in lists (timestamp, x, y, pupil size)
        tmp_DF = []
        print(f'processing trial # {trial_number}...')

    # This file records binocular data, for simplicity,
    # here we extract the left-eye samples only. A sample data line
    # always starts with an integer
    if trial_start and re.search('^\d', line):
        # 80855874	 1506.4	  269.0	  729.0	...
        # 80855875	   .	   .	    0.0	...
        if len(tmp_data) == 8:  # normal sample line
            tmp_DF.append(tmp_data[0:4])
        else:  # sample line with missing values (e.g., tracking loss)
            d_FRM.append([tmp_data[0], np.nan, np.nan, np.nan])

    if re.search('image_offset', line):  # message marking image offset
        # Put samples in a pandas data frame and store it in trial_DFs
        smp_colname = ['timestamp', 'gaze_x', 'gaze_y', 'pupil']
        trial_DFs[trial_number] = pd.DataFrame(tmp_DF, columns=smp_colname)
        trial_start = False

asc.close()  # close the ASC file

# Plot the gaze trace and pupil size data from trial # 1
trial_DFs[1].plot(y=['gaze_x', 'gaze_y', 'pupil'])
plt.show()
