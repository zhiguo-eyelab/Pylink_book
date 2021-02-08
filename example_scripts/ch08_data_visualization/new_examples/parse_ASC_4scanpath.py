#!/usr/bin/env python3
#
# Filename: parse_ASC_4scanpath.py
# Author: Zhiguo Wang
# Date: 2/8/2021
#
# Description:
# Parse the ASC file to extract fixations, then plot the scan path.

import os
from PIL import Image, ImageDraw
from math import sqrt

# Open the converted ASC file
asc = open(os.path.join('freeview', 'freeview.asc'))

trial_start = False
trial_number = 0
for line in asc:
    # Convert the current data line into a list
    tmp_data = line.rstrip().split()

    # Get screen resolution from the GAZE_COORDS message
    # MSG	4302897 GAZE_COORDS 0.00 0.00 1279.00 799.00
    if 'GAZE_COORDS' in line:
        scn_w = int(float(tmp_data[-2]) + 1)
        scn_h = int(float(tmp_data[-1]) + 1)

    # Message marking image onset
    if 'image_onset' in line:
        trial_start = True
        trial_number += 1
        bg_image = None
        # Store the position of all fixations in a list
        fix_coords = []
        # Store the duration of all fixations in a list
        fix_duration = []
        print(f'Processing trial # {trial_number} ...')

    if trial_start:
        # Get background image path
        # MSG	3558923 !V IMGLOAD FILL images\woods.jpg
        if 'IMGLOAD' in line:
           bg_image = line.rstrip().split()[-1]

        # Retrieve the coordinates and duration of all fixation
        # retrieve events from the right eye recording only
        # EFIX R 80790054 80790349 296 981.3 554.5 936 63.50 63.50
        if 'EFIX R' in line:
           duration, x, y = [int(float(x)) for x in tmp_data[4:7]]
           fix_coords.append((x, y))
           fix_duration.append(duration)

    # Message marking image offset
    if 'image_offset' in line:
        # Open the image and resize it to fill up the screen
        bg = Image.open(os.path.join('freeview', bg_image))
        bg = bg.resize((scn_w, scn_h))

        # create a ImageDraw object
        draw = ImageDraw.Draw(bg)

        # Draw the scan path
        draw.line(fix_coords, fill=(0, 0, 255), width=2)

        # Draw circles to represent the fixations
        for i, d in enumerate(fix_duration):
           sz = sqrt(d/max(fix_duration)*256)
           gx, gy = fix_coords[i]
           draw.ellipse([gx-sz, gy-sz, gx+sz, gy+sz],
                        fill=(255, 255, 0), outline=(0, 0, 255))

        # Save the scanpath for each trial
        bg.save(f'trial_{trial_number}.png', 'PNG')

# Close the ASC file
asc.close()
