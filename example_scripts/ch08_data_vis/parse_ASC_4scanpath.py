# Filename: parse_ASC_4scanpath.py

import os
from PIL import Image, ImageDraw

# path to the EDF data file
edf_dir = 'Picture/results/zw/'
# open converted ASC file
asc = open(edf_dir + 'zw.asc', 'r')

trial_start = False
trial_number = 0 
for line in asc:
    # convert the current data line into a list
    tmp_data = line.split()

# get screen resolution
if 'GAZE_COORDS' in line:
    scn_w, scn_h = [int(float(x)) + 1 for x in tmp_data[-2:]]

    # message marking image onset
    if 'SYNCTIME' in line: 
        trial_start = True
        trial_number += 1
        bg_image = None
        # store all fixations in a list
        fixations = []
        # store all fixation durations in a list
        fix_duration = [] 
        print('Processing trial # %d ...'%trial_number)
        
    if trial_start:
        # get background image from the .VCL file
        # MSG 80790106 -3 !V DRAW_LIST ../../runtime/dataviewer/zw/graphics/VC_1.vcl
        if 'DRAW_LIST' in line:
            # open the VCL file
            vcl = open(edf_dir + tmp_data[-1], 'r')
            for draw_commands in vcl:
                # looking for the IMGLOAD command
                # MSG 0 IMGLOAD TOP_LEFT  ../../runtime/images/5495090083862704888.png 0 0 1920 1080
                if 'IMGLOAD' in draw_commands:
                    tmp_list = draw_commands.split()
                    bg_image = [s for s in tmp_list if 'png' in s][0]
            # close the VCL file
            vcl.close() 

        # retrieve the coordinates and duration of all fixation
        # EFIX R 80790054 80790349 296 981.3 554.5 936 63.50 63.50
        if 'EFIX' in line:
            duration, x, y = [int(float(x)) for x in tmp_data[4:7]]
            fixations.append((x, y))
            fix_duration.append(duration)

    # message marking image offset   
    if 'blank_screen' in line: 
        bg = Image.open(edf_dir + bg_image)
        draw = ImageDraw.Draw(bg)
        # draw the scan path
        draw.line(fixations, fill=(0,0,255), width=3)
        # draw circles to represent the duration of the fixation
        for i, d in enumerate(fix_duration):
            sz = int(d/max(fix_duration)*30)
            gx, gy = fixations[i]
            draw.ellipse([(gx-sz, gy-sz), (gx+sz, gy+sz)],fill=(0,0,255))
        # save the scanpath for each trial
        bg.save('trial_%d.png'%trial_number, 'PNG')

# close the ASC file 
asc.close()       
