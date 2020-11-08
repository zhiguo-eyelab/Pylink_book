# Filename: gaze_trace_plot.py

import os, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

edf_dir = 'Picture/results/zw/' # path to the EDF data file
os.system('edf2asc -y %s' %(edf_dir + 'zw.edf')) # convert the EDF
asc = open(edf_dir + 'zw.asc', 'r') # open converted ASC file

scn_w, scn_h = [-32768, -32768]
trial_start = False
trial_DFs = {} # data frames from all trials in a tuple
trial_number = 0
for line in asc:
    # extract values from data lines
    tmp_data = [float(x) for x in re.findall(r'-?\d+\.?\d*', line)]
    
    # message marking image onset
    if re.search('SYNCTIME', line): 
        trial_start = True
        trial_number += 1
        t = []; x =[]; y =[]; p =[] # store sample data in lists
        print('processing trial # %d...' %trial_number)

    # sample lines always start with timestamps
    if trial_start and re.search('^\d', line): 
        # 80855874	 1506.4	  269.0	  729.0	...
        # 80855875	   .	   .	    0.0	...
        if len(tmp_data) == 4: # normal sample line
            s_t, s_x, s_y, s_pu = tmp_data
        else:
            st, s_pu = tmp_data # missing samples
            s_x = np.nan; s_y = np.nan
        t.append(s_t); x.append(s_x); y.append(s_y); p.append(s_pu)
          
    if re.search('blank_screen', line): # message marking image offset
        # put samples in a pandas data frame and store it in trial_DFs
        trial_DFs[trial_number] = pd.DataFrame({'timestamp': t, \
                                                'gaze_x': x, 'gaze_y': y, \
                                                'pupil': p})
        trial_start = False

asc.close() # close the ASC file

# plot the gaze trace and pupil size data from trial # 4
trial_DFs[4].plot(y=['gaze_x', 'gaze_y', 'pupil'])
plt.show()
