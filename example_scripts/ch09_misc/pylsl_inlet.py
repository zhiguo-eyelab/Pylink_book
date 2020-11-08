import time
import pylsl

# look for an EyeLink data stream on the lab network
print("looking for an Eyelink data stream...")
streams = pylsl.resolve_stream('type', 'Gaze')
 
# create a new inlet to read data from the stream
inlet = pylsl.StreamInlet(streams[0], max_buflen=1)
 
# Record data for 10 seconds
print('Reading ...')
record_start = time.time()
sample_time = 0
while True:
    sample, timestamp = inlet.pull_sample(timeout=0)
 
    # if a new sample is recieved, print it out
    if sample:
        if sample[-2]>sample_time:
            print(sample)
            sample_time = sample[-2]

    if time.time() - record_start > 10.0:
        break
