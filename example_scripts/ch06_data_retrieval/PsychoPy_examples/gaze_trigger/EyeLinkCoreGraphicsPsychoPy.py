#!/usr/bin/env python3
#
# Filename: EyeLinkCoreGraphicsPsychoPy.py
# Author: Zhiguo Wang
# Date: 2/4/2021
#
# Description:
# An EyeLink coregraphics library (calibration routine)
# for PsychoPy experiments.

import os
import platform
import array
import string
import pylink
from psychopy import visual, event, core
from math import sin, cos, pi
from PIL import Image, ImageDraw
from psychopy.sound import Sound


class EyeLinkCoreGraphicsPsychoPy(pylink.EyeLinkCustomDisplay):
    def __init__(self, tracker, win):
        '''Initialize

        tracker: an EyeLink instance (connection)
        win: the PsychoPy window we use for calibration'''

        pylink.EyeLinkCustomDisplay.__init__(self)

        # background and target color
        self._backgroundColor = win.color
        self._foregroundColor = 'black'

        # window to use for calibration
        self._display = win
        # make the mouse cursor invisible
        self._display.mouseVisible = False

        # display width & height
        self._w, self._h = win.size

        # resolution fix for Mac retina displays
        if 'Darwin' in platform.system():
            sys_cmd = 'system_profiler SPDisplaysDataType | grep Retina'
            is_ret = os.system(sys_cmd)
            if is_ret == 0:
                self._w = int(self._w / 2.0)
                self._h = int(self._h / 2.0)

        # store camera image pixels in an array
        self._imagebuffer = array.array('I')

        # store the color palette for camera image drawing
        self._pal = None

        # initial size of the camera image
        self._size = (384, 320)

        # initial mouse configuration
        self._mouse = event.Mouse(False)
        self.last_mouse_state = -1

        # camera image title
        self._msgHeight = self._size[1]/16.0
        self._title = visual.TextStim(self._display, '',
                                      wrapWidth=self._w,
                                      color=self._foregroundColor)

        # calibration target
        self._targetSize = self._w/64.
        self._tar = visual.Circle(self._display,
                                  size=self._targetSize,
                                  lineColor=self._foregroundColor,
                                  lineWidth=self._targetSize/2)

        # calibration sounds (beeps)
        self._target_beep = Sound('type.wav', stereo=True)
        self._error_beep = Sound('error.wav', stereo=True)
        self._done_beep = Sound('qbeep.wav', stereo=True)

        # a reference to the tracker connection
        self._tracker = tracker

        # for a clearer view we always enlarge the camera image
        self.imgResize = None

    def setup_cal_display(self):
        '''Set up the calibration display '''

        self._display.clearBuffer()

    def clear_cal_display(self):
        '''Clear the calibration display'''

        self._display.color = self._backgroundColor
        self._display.flip()

    def exit_cal_display(self):
        '''Exit the calibration/validation routine'''

        self.clear_cal_display()

    def record_abort_hide(self):
        '''This function is called if aborted'''

        pass

    def erase_cal_target(self):
        '''Erase the target'''

        self.clear_cal_display()

    def draw_cal_target(self, x, y):
        '''Draw the target'''

        self.clear_cal_display()

        # target position
        xVis = (x - self._w/2.0)
        yVis = (self._h/2.0 - y)

        # draw the calibration target
        self._tar.pos = (xVis, yVis)
        self._tar.draw()
        self._display.flip()

    def play_beep(self, beepid):
        ''' Play a sound during calibration/drift-correction.'''

        if beepid in [pylink.CAL_TARG_BEEP, pylink.DC_TARG_BEEP]:
            self._target_beep.play()
        elif beepid in [pylink.CAL_ERR_BEEP, pylink.DC_ERR_BEEP]:
            self._error_beep.play()
        elif beepid in [pylink.CAL_GOOD_BEEP, pylink.DC_GOOD_BEEP]:
            self._done_beep.play()
        core.wait(0.4)

    def getColorFromIndex(self, colorindex):
        '''Retrieve the colors for camera image elements, e.g., crosshair'''

        if colorindex == pylink.CR_HAIR_COLOR:
            return (255, 255, 255)
        elif colorindex == pylink.PUPIL_HAIR_COLOR:
            return (255, 255, 255)
        elif colorindex == pylink.PUPIL_BOX_COLOR:
            return (0, 255, 0)
        elif colorindex == pylink.SEARCH_LIMIT_BOX_COLOR:
            return (255, 0, 0)
        elif colorindex == pylink.MOUSE_CURSOR_COLOR:
            return (255, 0, 0)
        else:
            return (128, 128, 128)

    def draw_line(self, x1, y1, x2, y2, colorindex):
        '''Draw a line '''

        color = self.getColorFromIndex(colorindex)

        # scale the coordinates
        w, h = self._img.im.size
        x1 = int(x1 / 192 * w)
        x2 = int(x2 / 192 * w)
        y1 = int(y1 / 160 * h)
        y2 = int(y2 / 160 * h)

        # draw the line
        if not any([x < 0 for x in [x1, x2, y1, y2]]):
            self._img.line([(x1, y1), (x2, y2)], color)

    def draw_lozenge(self, x, y, width, height, colorindex):
        ''' draw a lozenge to show the defined search limits '''

        color = self.getColorFromIndex(colorindex)

        # scale the coordinates
        w, h = self._img.im.size
        x = int(x / 192 * w)
        y = int(y / 160 * h)
        width = int(width / 192 * w)
        height = int(height / 160 * h)

        # draw the lozenge
        if width > height:
            rad = int(height / 2.)
            if rad == 0:
                return
            else:
                self._img.line([(x + rad, y), (x + width - rad, y)], color)
                self._img.line([(x + rad, y + height),
                                (x + width - rad, y + height)], color)
                self._img.arc([x, y, x + rad*2, y + rad*2], 90, 270, color)
                self._img.arc([x + width - rad*2, y, x + width, y + height],
                              270, 90, color)
        else:
            rad = int(width / 2.)
            if rad == 0:
                return
            else:
                self._img.line([(x, y + rad), (x, y + height - rad)], color)
                self._img.line([(x + width, y + rad),
                                (x + width, y + height - rad)], color)
                self._img.arc([x, y, x + rad*2, y + rad*2], 180, 360, color)
                self._img.arc([x, y + height-rad*2, x + rad*2, y + height],
                              0, 180, color)

    def get_mouse_state(self):
        '''Get the current mouse position and status'''

        w, h = self._display.size
        X, Y = self._mouse.getPos()

        # scale the mouse position so the cursor stay on the camera image
        mX = (X + w/2.0)/w*self._size[0]/2.0
        mY = (h/2.0 - Y)/h*self._size[1]/2.0

        state = self._mouse.getPressed()[0]

        return ((mX, mY), state)

    def get_input_key(self):
        '''This function is repeatedly pooled to check
        keyboard events'''

        ky = []
        for keycode, modifier in event.getKeys(modifiers=True):
            k = pylink.JUNK_KEY
            if keycode == 'f1': k = pylink.F1_KEY
            elif keycode == 'f2': k = pylink.F2_KEY
            elif keycode == 'f3': k = pylink.F3_KEY
            elif keycode == 'f4': k = pylink.F4_KEY
            elif keycode == 'f5': k = pylink.F5_KEY
            elif keycode == 'f6': k = pylink.F6_KEY
            elif keycode == 'f7': k = pylink.F7_KEY
            elif keycode == 'f8': k = pylink.F8_KEY
            elif keycode == 'f9': k = pylink.F9_KEY
            elif keycode == 'f10': k = pylink.F10_KEY
            elif keycode == 'pageup': k = pylink.PAGE_UP
            elif keycode == 'pagedown': k = pylink.PAGE_DOWN
            elif keycode == 'up': k = pylink.CURS_UP
            elif keycode == 'down': k = pylink.CURS_DOWN
            elif keycode == 'left': k = pylink.CURS_LEFT
            elif keycode == 'right': k = pylink.CURS_RIGHT
            elif keycode == 'backspace': k = ord('\b')
            elif keycode == 'return': k = pylink.ENTER_KEY
            elif keycode == 'space': k = ord(' ')
            elif keycode == 'escape': k = 27
            elif keycode == 'tab': k = ord('\t')
            elif keycode in string.ascii_letters:
                k = ord(keycode)
            elif k == pylink.JUNK_KEY:
                k = 0

            # plus & minus signs for CR adjustment
            if keycode in ['num_add', 'equal']:
                k = ord('+')
            if keycode in ['num_subtract', 'minus']:
                k = ord('-')

            # handles key modifier
            if modifier['alt'] is True: mod = 256
            elif modifier['ctrl'] is True: mod = 64
            elif modifier['shift'] is True: mod = 1
            else:
                mod = 0

            ky.append(pylink.KeyInput(k, mod))

        return ky

    def exit_image_display(self):
        '''Clear the camera image'''

        self.clear_cal_display()
        self._display.flip()

    def alert_printf(self, msg):
        '''Print error messages.'''

        print("Error: " + msg)

    def setup_image_display(self, width, height):
        ''' set up the camera image

        return 1 to show high-resolution camera images'''

        self.last_mouse_state = -1
        self._size = (width, height)

        return 1

    def image_title(self, text):
        '''Draw title text below the camera image'''

        self._title.text = text

    def draw_image_line(self, width, line, totlines, buff):
        '''Display image pixel by pixel, line by line'''

        for i in range(width):
            try:
                self._imagebuffer.append(self._pal[buff[i]])
            except:
                pass

        if line == totlines:
            bufferv = self._imagebuffer.tostring()
            img = Image.frombytes("RGBX", (width, totlines), bufferv)
            self._img = ImageDraw.Draw(img)
            # draw the cross hairs
            self.draw_cross_hair()
            # scale the camera image
            self.imgResize = img.resize((width*2, totlines*2))
            cam_img = visual.ImageStim(self._display,
                                       image=self.imgResize,
                                       units='pix')
            cam_img.draw()
            # draw the camera image title
            self._title.pos = (0, - totlines - self._msgHeight)
            self._title.draw()
            self._display.flip()

            # clear the camera image buffer
            self._imagebuffer = array.array('I')

    def set_image_palette(self, r, g, b):
        '''Given a set of RGB colors, create a list of 24bit numbers
        representing the color palette.
        For instance, RGB of (1,64,127) would be saved as 82047,
        or 00000001 01000000 011111111'''

        self._imagebuffer = array.array('I')

        sz = len(r)
        i = 0
        self._pal = []
        while i < sz:
            rf = int(b[i])
            gf = int(g[i])
            bf = int(r[i])
            self._pal.append((rf << 16) | (gf << 8) | (bf))
            i = i+1
