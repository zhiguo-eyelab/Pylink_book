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

# Open the converted ASC file
asc = open(os.path.join('freeview', 'freeview.asc'))

efix = []  # fixation end events
esac = []  # saccade end events
for line in asc:
    # Extract all numbers and put them in a list
    tmp_data = [float(x) for x in re.findall(r'-?\d+\.?\d*', line)]

    # retrieve events parsed from the right eye recording
    if re.search('^EFIX R', line):
        efix.append(tmp_data)
    elif re.search('^ESACC R', line):
        esac.append(tmp_data)
    else:
        pass

# Put the extracted data into pandas data frames
# EFIX R 80790054 80790349 296 981.3 554.5 936
efix_colname = ['startT', 'endT', 'duration', 'avgX', 'avgY', 'avgPupil']
efixFRM = pd.DataFrame(efix, columns=efix_colname)
# ESACC R 80790350 80790372 23 982.6 551.8 864.9 587.9 1.94 151
esac_colname = ['startT', 'endT', 'duration', 'startX', 'startY',
                'endX', 'endY', 'amplitude', 'peakVel']
esacFRM = pd.DataFrame(esac, columns=esac_colname)

# Close the ASC file
asc.close()
