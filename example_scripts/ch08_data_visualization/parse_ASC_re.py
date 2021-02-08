#!/usr/bin/env python3
#
# Filename: parse_ASC_re.py
# Author: Zhiguo Wang
# Date: 2/8/2021
#
# Description:
# Parse the ASC file with regular expressions (re).

import os
import re
import pandas as pd

# Path to the EDF data file
edf_dir = 'Picture/results/zw/'
# Convert the edf file
os.system('edf2asc -e -y %s' % (edf_dir + 'zw.edf'))
# Open converted ASC file
asc = open(edf_dir + 'zw.asc', 'r')

efix = []  # fixation end
esac = []  # saccade end
for line in asc:
    # Extract all numbers and put it in a list
    tmp_data = [float(x) for x in re.findall(r'-?\d+\.?\d*', line)]

    if re.search('^EFIX', line):
        efix.append(tmp_data)
    elif re.search('^ESACC', line):
        esac.append(tmp_data)
    else:
        pass

# Put the extracted data into pandas data frames
# EFIX R 80790054 80790349 296 981.3 554.5 936
efixFRM = pd.DataFrame(efix, columns=['startT', 'endT', 'duration',
                                      'avgX', 'avgY', 'pupil'])
# ESACC R 80790350 80790372 23 982.6 551.8 864.9 587.9 1.94 151
esacFRM = pd.DataFrame(esac, columns=['startT', 'endT', 'duration',
                                      'startX', 'startY', 'endX',
                                      'endY', 'amplitude', 'peakVel'])

# Close the ASC file
asc.close()
