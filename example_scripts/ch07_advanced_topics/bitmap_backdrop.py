#!/usr/bin/env python3
#
# Filename: bitmap_backdrop.py
# Author: Zhiguo Wang
# Date: 2/5/2020
#
# Description:
# Transfer an image to the Host to use as the backdrop

import pylink
from PIL import Image

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Put the tracker in offline mode before we transfer the image
tk.setOfflineMode()

# convert the image to the <pixel> format supported by
# the bitmapBackdrop() command
im = Image.open('quebec.jpeg')  # open an image with PIL
w, h = im.size  # get the width and height of an image
pixels = im.load()  # access the pixel data
# reformat the pixels 
pixels_img = [[pixels[i, j] for i in range(w)] for j in range(h)]

# Construct an image in <pixel> format with RGB tuples
white_rgb = (255, 255, 255)
black_rgb = (0, 0, 0)
pixels_rgb = [
    [black_rgb, black_rgb, black_rgb, white_rgb, white_rgb, white_rgb],
    [black_rgb, black_rgb, black_rgb, white_rgb, white_rgb, white_rgb],
    [black_rgb, black_rgb, black_rgb, white_rgb, white_rgb, white_rgb],
    [white_rgb, white_rgb, white_rgb, black_rgb, black_rgb, black_rgb],
    [white_rgb, white_rgb, white_rgb, black_rgb, black_rgb, black_rgb],
    [white_rgb, white_rgb, white_rgb, black_rgb, black_rgb, black_rgb],
    ]*100

# construct an image in <pixel> format with hexadecimal values
# i.e., alpha-R-G-B
white_hex = 0x00FFFFFF
black_hex = 0x0
pixels_hex = [
    [black_hex, black_hex, black_hex, white_hex, white_hex, white_hex],
    [black_hex, black_hex, black_hex, white_hex, white_hex, white_hex],
    [black_hex, black_hex, black_hex, white_hex, white_hex, white_hex],
    [white_hex, white_hex, white_hex, black_hex, black_hex, black_hex],
    [white_hex, white_hex, white_hex, black_hex, black_hex, black_hex],
    [white_hex, white_hex, white_hex, black_hex, black_hex, black_hex],
    ]*100

# Transfer the images to the Host PC screen
tk.sendCommand('clear_screen 0')
tk.sendCommand('echo PIXELs_FROM_IMAGE')
tk.bitmapBackdrop(w, h, pixels_img, 0, 0, w, h,
                  50, 50, pylink.BX_MAXCONTRAST)

# Show the image for 3-sec on the Host PC
pylink.msecDelay(3000)

# Transfer the checkerboard constructed with Hex values to the Host
# show it at (250, 0) for 3-sec
tk.sendCommand('clear_screen 0')
tk.sendCommand('echo PIXELs_FROM_HEX')
tk.bitmapBackdrop(6, 600, pixels_hex, 0, 0, 6, 600,
                  250, 0, pylink.BX_MAXCONTRAST)

# Show the image for 3-sec on the Host PC
pylink.msecDelay(3000)

# Transfer the checkerboard constructed with RGB tuples to the Host
# show it at (250, 0) for 3 sec
tk.sendCommand('clear_screen 0')
tk.sendCommand('echo PIXELs_FROM_RGB')
tk.bitmapBackdrop(6, 600, pixels_rgb, 0, 0, 6, 600,
                  250, 0, pylink.BX_MAXCONTRAST)

pylink.msecDelay(3000)

# Clear up the Host screen
tk.sendCommand('clear_screen 0')

# Close the connection
tk.close()
