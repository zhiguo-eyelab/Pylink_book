# Filename: parse_ASC_re.py

import os, re
import pandas as pd

# path to the EDF data file
edf_dir = 'Picture/results/zw/'
# conver the edf file
os.system('edf2asc -e -y %s' %(edf_dir + 'zw.edf'))
# open converted ASC file
asc = open(edf_dir + 'zw.asc', 'r') 

efix = [] # fixation end
esac = [] # saccade end
for line in asc:
    # extract all numbers and put it in a list
    tmp_data = [float(x) for x in re.findall(r'-?\d+\.?\d*', line)]
    
    if re.search('^EFIX', line):
        efix.append(tmp_data)
    elif re.search('^ESACC', line):
        esac.append(tmp_data)
    else:
        pass
    
# put the extracted data into pandas data frames
# EFIX R 80790054 80790349 296 981.3 554.5 936
efixFRM = pd.DataFrame(efix,columns=['startT', 'endT', 'duration',
                                     'avgX', 'avgY', 'pupil'])
# ESACC R 80790350 80790372 23 982.6 551.8 864.9 587.9 1.94 151
esacFRM = pd.DataFrame(esac,columns=['startT', 'endT', 'duration',
                                     'startX', 'startY', 'endX',
                                     'endY', 'amplitude', 'peakVel'])

