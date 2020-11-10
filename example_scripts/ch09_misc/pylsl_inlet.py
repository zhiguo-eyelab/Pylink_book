# Filename: pylsl_inlet.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# Receiving data with an LSL inlet

import time
import pylsl

# Look for an EyeLink data stream on the network
print("Looking for an Eyelink data stream...")
streams = pylsl.resolve_stream('type', 'Gaze')
 
# Create a new inlet to read data from the stream
inlet = pylsl.StreamInlet(streams[0], max_buflen=1)
 
# Record data for 10 seconds
print('Reading ...')
record_start = time.time()
sample_time = 0
while True:
    sample, timestamp = inlet.pull_sample(timeout=0)
 
    # If a new sample is recieved, print it out
    if sample:
        if sample[-2]>sample_time:
            print(sample)
            sample_time = sample[-2]

    if time.time() - record_start > 10.0:
        break
