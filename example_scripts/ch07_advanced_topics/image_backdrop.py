# Filename: image_backdrop.py

import pylink
from PIL import Image

# open a connection to the tracker
tk = pylink.EyeLink('100.1.1.1')
# set the tracker to offline mode
tk.setOfflineMode()

# convert an image to the <pixel> format supported by the bitmapBackdrop command
im = Image.open('sacrmeto.bmp') # open an image with PIL
w,h = im.size # get the width and height of an image
pixels = im.load() # load to access pixel data
pixels_2transfer = [[pixels[i,j] for i in range(w)] for j in range(h)]

# construct an image in <pixel> format with RGB tuples
pixels_RGB = [[(0,0,0), (0,0,0),(0,0,0),(255,255,255),(255,255,255),(255,255,255)],
                [(0,0,0), (0,0,0),(0,0,0),(255,255,255),(255,255,255),(255,255,255)],
                [(0,0,0), (0,0,0),(0,0,0),(255,255,255),(255,255,255),(255,255,255)],
                [(255,255,255), (255,255,255),(255,255,255),(0,0,0),(0,0,0),(0,0,0)],
                [(255,255,255), (255,255,255),(255,255,255),(0,0,0),(0,0,0),(0,0,0)],
                [(255,255,255), (255,255,255),(255,255,255),(0,0,0),(0,0,0),(0,0,0)]]

# construct an image in <pixel> format with hexadecimal values alpha-R-G-B
pixels_HEX = [[0x0,0x0,0x0,0x00FFFFFF,0x00FFFFFF,0x00FFFFFF],
                [0x0,0x0,0x0,0x00FFFFFF,0x00FFFFFF,0x00FFFFFF],
                [0x0,0x0,0x0,0x00FFFFFF,0x00FFFFFF,0x00FFFFFF],
                [0x00FFFFFF,0x00FFFFFF,0x00FFFFFF,0x0,0x0,0x0],
                [0x00FFFFFF,0x00FFFFFF,0x00FFFFFF,0x0,0x0,0x0],
                [0x00FFFFFF,0x00FFFFFF,0x00FFFFFF,0x0,0x0,0x0]]

# transfer one of the above images to the Host PC screen
tk.sendCommand('clear_screen 0')
#tk.bitmapBackdrop(w, h, pixels_2transfer, 0, 0, w, h, 0, 0, pylink.BX_MAXCONTRAST)
tk.bitmapSaveAndBackdrop(w, h, pixels_2transfer, 0, 0, w, h, 'trial_image', 'img',
                         pylink.SV_MAKEPATH, 0, 0, pylink.BX_MAXCONTRAST)
                         
#tk.bitmapBackdrop(6, 6, pixels_HEX, 0, 0, 6, 6, 0, 0, pylink.BX_MAXCONTRAST)
#tk.bitmapSaveAndBackdrop(6, 6, pixels_HEX, 0, 0, 6, 6, 'trial_image', 'img',
#                         pylink.SV_MAKEPATH, 300, 300, pylink.BX_MAXCONTRAST)

# close the connection
tk.close()
