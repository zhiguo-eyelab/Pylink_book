# Filename: heatmap_simple.py

import os, re
from PIL import Image
import numpy as np
from matplotlib import cm # colormap from matplotlib

edf_dir = 'Picture/results/zw/' # path to the EDF data file
os.system('edf2asc -e -y -res %s' %(edf_dir + 'zw.edf')) # convert the EDF
asc = open(edf_dir + 'zw.asc', 'r') # open converted ASC file

scn_w, scn_h = [-32768, -32768]
trial_start = False
trial_number = 0
for line in asc:
    # extract values from data lines
    tmp_data = [int(float(x)) for x in re.findall(r'-?\d+\.?\d*', line)]
    
    if re.search('GAZE_COORDS', line): # get screen resolution
        scn_w, scn_h = [int(x+1) for x in tmp_data[-2:]]
    if re.search('SYNCTIME', line): # message marking image onset
        trial_start = True
        trial_number += 1
        print('processing trial # %d...' %trial_number)

        sigma_x, sigma_y = (0.1, 0.1) # width of the 2-D gaussian-Y        
        alpha = 0.5  # transparency for the heatmap 
        w, h = np.meshgrid(np.linspace(0,scn_w,scn_w), \
                           np.linspace(0,scn_h,scn_h))
        heatmap = 0.0*np.exp(-1.0*(w-0)**2/(2*sigma_x**2)-\
                             1.0*(h-0)**2/(2*sigma_y**2))
        
    if trial_start:
        if re.search('^EFIX', line): # add fixation summary data to efix
            # EFIX R 80790373 80790527 155 855.5 596.0 881 63.60 63.75
            start_t, end_t, duration, gaze_x, gaze_y, peak_vel, sigma_x, sigma_y = tmp_data
            heatmap += duration*np.exp(-1.0*(w-gaze_x)**2/(2*sigma_x**2)-\
                                       1.0*(h-gaze_y)**2/(2*sigma_y**2))
            
        # get background image from the .VCL file
        if re.search('DRAW_LIST', line): 
            # MSG 80790106 -3 !V DRAW_LIST ../../runtime/dataviewer/
            # zw/graphics/VC_1.vcl
            vcl = open(edf_dir + line.split()[-1], 'r')
            for draw_commands in vcl:
                if 'IMGLOAD' in draw_commands:
                    # 0 IMGLOAD TOP_LEFT  ../../runtime/images/
                    # 5495090083862704888.png 0 0 1920 1080
                    # get the path to the .png image
                    bg_image = draw_commands.split()[3] 
            vcl.close() # close VCL file
            
    if re.search('blank_screen', line): # message marking image offset
        background_pic = Image.open(edf_dir + bg_image).convert('RGBA')
        # apply a colormap (from the colormap library in MatplotLib)
        heatmap = heatmap/np.max(heatmap)
        heatmap = Image.fromarray(np.uint8(cm.seismic(heatmap)*255))
        heatmap = heatmap.convert('RGBA')
        heatmap = Image.blend(background_pic, heatmap, alpha) # blending
        # save the heatmap as an PNG file
        heatmap.save('heatmap_trial_%d.png'%trial_number, 'PNG') 
        trial_start = False

asc.close() # close the ASC file
