#!/usr/bin/env python3
#
# Filename: get_fontNames.py
# Author: Zhiguo Wang
# Date: 2/7/2020
#
# Description:
# Retrieve the names of all available system fonts
# Run this script from the command line

from matplotlib import font_manager

f_list = font_manager.get_fontconfig_fonts()
f_names = []
for font in f_list:
    try:
        f = font_manager.FontProperties(fname=font).get_name()
        f_names.append(f)
    except:
        pass

print(f_names)
