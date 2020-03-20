# Filename: monitor_gamma.py

from psychopy import monitors
import matplotlib.pyplot as plt

# photometer measurements
pix_inp = [0, 16, 32, 48, 64, 80, 96, 112, 128, 144,
           160, 176, 192, 208, 224, 240, 255]
lum = [6.08,8.2,11.4,15.8,21.59,28.73,37.32,47.4,59.14,
       71.43,86.3,102.4,120.9,141.5,166.7,188.6,214.8]

# create a GammaCalculator
g_cal = monitors.GammaCalculator(pix_inp, lum)
# fit the gamma function
g_cal.fitGammaFun(pix_inp, lum)
# print out the fited gamma value
print(g_cal.gamma) 

# generate data points for the fitted gamma function and plot
g_fun = monitors.gammaFun(pix_inp, lum[0], lum[-1], g_cal.gamma)
plt.plot(pix_inp, g_fun, 'k-', lw=2)
plt.xlabel('Pixel bit value')
plt.ylabel('Luminance (cd/m^2)')
plt.show()

