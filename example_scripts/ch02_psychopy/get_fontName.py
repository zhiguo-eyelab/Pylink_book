# Filename: get_fontNames.py
# Author: Zhiguo Wang
# Date: 2/3/2020
#
# Description:
# Retrieve the names of all available system fonts

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
