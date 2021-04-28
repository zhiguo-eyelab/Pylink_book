#!/usr/bin/env python3
#
# Filename: bitmap_backdrop.py
# Author: Zhiguo Wang
# Date: 4/27/2021
#
# Description:
# Transfer an image to the Host to use as the backdrop

import pylink
from PIL import Image

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Pass display dimension (left, top, right, bottom) to the tracker
tk.sendCommand('screen_pixel_coords = 0 0 1023 767')

# Put the tracker in offline mode before we transfer the image
tk.setOfflineMode()

# convert the image to the <pixel> format supported by
# the bitmapBackdrop() command
im = Image.open('quebec.jpeg')  # open an image with PIL
w, h = im.size  # get the width and height of the image
pixels = im.load()  # access the pixel data
# reformat the pixels 
pixels_img = [[pixels[i, j] for i in range(w)] for j in range(h)]

# Transfer the images to the Host PC screen
tk.sendCommand('clear_screen 0')
tk.sendCommand('echo PIXELs_FROM_IMAGE')
tk.bitmapBackdrop(w, h, pixels_img, 0, 0, w, h,
                  50, 50, pylink.BX_MAXCONTRAST)

# Show the image for 3-sec on the Host PC
pylink.msecDelay(3000)

# Clear up the Host screen
tk.sendCommand('clear_screen 0')

# Close the connection
tk.close()
