#!/usr/bin/env python3
#
# Filename: parse_ASC_4scanpath.py
# Author: Zhiguo Wang
# Date: 5/25/2021
#
# Description:
# Parse an ASC file to extract fixations, then plot the scanpath.

import os
from PIL import Image, ImageDraw
from math import sqrt

# Open the converted ASC file
asc = open(os.path.join('freeview', 'freeview.asc'))

new_trial = False
trial = 0
for line in asc:
    # Convert the current data line into a list
    tmp_data = line.rstrip().split()

    # Get the correct screen resolution from the DISPLAY_COORDS message
    # MSG	4302897 DISPLAY_COORDS 0 0 1279 799
    if 'DISPLAY_COORDS' in line:
        scn_w = int(tmp_data[-2]) + 1
        scn_h = int(tmp_data[-1]) + 1

    # Look for the message marking image onset
    if 'image_onset' in line:
        new_trial = True
        trial += 1
        print(f'Processing trial # {trial} ...')

        # Store the position and duration of all fixations in lists
        fix_coords = []
        fix_duration = []

    if new_trial:
        # Path to the background image
        # MSG	3558923 !V IMGLOAD FILL images/woods.jpg
        if 'IMGLOAD' in line:
            bg_image = tmp_data[-1]

        # Retrieve the coordinates and duration of all fixations
        # EFIX R 80790054 80790349 296 981.3 554.5 936 63.50 63.50
        if 'EFIX' in line:
            duration, x, y = [int(float(x)) for x in tmp_data[4:7]]
            fix_coords.append((x, y))
            fix_duration.append(duration)

    # Look for the message marking image offset, draw the scanpath
    if 'image_offset' in line:
        # Open the image and resize it to fill up the screen
        img = os.path.join('freeview', bg_image)
        pic = Image.open(img).resize((scn_w, scn_h))

        # Create an ImageDraw object
        draw = ImageDraw.Draw(pic)

        # Draw the scanpath
        draw.line(fix_coords, fill=(0, 0, 255), width=2)

        # Draw circles to represent the fixations, the diameter reflects
        # the fixation duration, scaled to its maximum
        for i, d in enumerate(fix_duration):
            sz = sqrt(d / max(fix_duration) * 256)
            gx, gy = fix_coords[i]
            draw.ellipse([gx-sz, gy-sz, gx+sz, gy+sz],
                         fill=(255, 255, 0), outline=(0, 0, 255))

        # Save the scanpath for each trial
        pic.save(f'scanpath_trial_{trial}.png', 'PNG')

# Close the ASC file
asc.close()
