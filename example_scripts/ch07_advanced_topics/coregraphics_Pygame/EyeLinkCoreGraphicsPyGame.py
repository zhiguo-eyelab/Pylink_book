# Filename: EyeLinkCoreGraphicsPygame.py
# Author: Zhiguo Wang
# Date: 11/9/2020
#
# Description:
# An example CoreGraphics library implemented in Pygame

import pygame
from pygame.locals import *
from math import pi
import array
import pylink


class EyeLinkCoreGraphicsPyGame(pylink.EyeLinkCustomDisplay):
    def __init__(self, tracker, win):
        pylink.EyeLinkCustomDisplay.__init__(self)

        self.win = win  # screen to use for calibration
        self.tracker = tracker  # connection to the tracker

        self.bgColor = (128, 128, 128)  # target color (foreground)
        self.fgColor = (0, 0, 0)  # target color (background)
        self.targetSize = 32  # diameter of the target

        self.enableBeep = True  # play warning beeps, True or False
        self.__target_beep__ = pygame.mixer.Sound("type.wav")
        self.__target_beep__done__ = pygame.mixer.Sound("qbeep.wav")
        self.__target_beep__error__ = pygame.mixer.Sound("error.wav")

        self.size = (384, 320)  # size of the camera image
        self.imagebuffer = array.array('I')  # buffer to store camera image

        # Image palette; we use its indices to recreate the camera image
        self.pal = []

        self.fnt = pygame.font.SysFont('Arial', 26)  # a font object

        self.last_mouse_state = -1

    def setup_cal_display(self):
        '''Setup calibration/validation display'''

        self.clear_cal_display()

    def exit_cal_display(self):
        '''Exit calibration/validation display'''

        self.clear_cal_display()

    def record_abort_hide(self):
        pass

    def clear_cal_display(self):
        '''Clear the screen for calibration '''

        self.win.fill(self.bgColor)
        pygame.display.flip()
        self.win.fill(self.bgColor)

    def erase_cal_target(self):
        ''' Erase the calibration target from the screen '''

        self.clear_cal_display()

    def draw_cal_target(self, x, y):
        ''' Draw the calibration target, i.e., a bull's eye'''

        pygame.draw.circle(self.win, self.fgColor, (x, y),
                           int(self.targetSize/2.))
        pygame.draw.circle(self.win, self.bgColor, (x, y),
                           int(self.targetSize/4.))
        pygame.display.flip()

    def play_beep(self, beepid):
        '''Play warning beeps if being requested'''

        if self.enableBeep:
            if beepid == pylink.DC_TARG_BEEP or
            beepid == pylink.CAL_TARG_BEEP:
                self.__target_beep__.play()
            elif beepid == pylink.CAL_ERR_BEEP or
            beepid == pylink.DC_ERR_BEEP:
                self.__target_beep__error__.play()
            else:  # CAL_GOOD_BEEP or DC_GOOD_BEEP
                self.__target_beep__done__.play()

    def getColorFromIndex(self, colorindex):
        ''' Color scheme for different elements '''

        if colorindex == pylink.CR_HAIR_COLOR:
            return (255, 255, 255, 255)
        elif colorindex == pylink.PUPIL_HAIR_COLOR:
            return (255, 255, 255, 255)
        elif colorindex == pylink.PUPIL_BOX_COLOR:
            return (0, 255, 0, 255)
        elif colorindex == pylink.SEARCH_LIMIT_BOX_COLOR:
            return (255, 0, 0, 255)
        elif colorindex == pylink.MOUSE_CURSOR_COLOR:
            return (255, 0, 0, 255)
        else:
            return (0, 0, 0, 0)

    def draw_line(self, x1, y1, x2, y2, colorindex):
        ''' Draw lines for crosshair etc.'''

        color = self.getColorFromIndex(colorindex)

        # Get the camera image rect, then scale
        if self.size[0] > 192:
            imr = self.__img__.get_rect()
            x1 = int((float(x1) / 192) * imr.w)
            x2 = int((float(x2) / 192) * imr.w)
            y1 = int((float(y1) / 160) * imr.h)
            y2 = int((float(y2) / 160) * imr.h)
        # Draw the line
        if True not in [x < 0 for x in [x1, x2, y1, y2]]:
            pygame.draw.line(self.__img__, color, (x1, y1), (x2, y2))

    def draw_lozenge(self, x, y, width, height, colorindex):
        ''' Draw the search limits with two lines and two arcs'''

        color = self.getColorFromIndex(colorindex)

        if self.size[0] > 192:
            imr = self.__img__.get_rect()
            x = int((float(x) / 192) * imr.w)
            y = int((float(y) / 160) * imr.h)
            width = int((float(width) / 192) * imr.w)
            height = int((float(height) / 160) * imr.h)

        if width > height:
            rad = int(height / 2.)
            if rad == 0:
                return
            else:
                pygame.draw.line(self.__img__, color,
                                 (x + rad, y), (x + width - rad, y))
                pygame.draw.line(self.__img__, color,
                                 (x + rad, y + height),
                                 (x + width - rad, y + height))
                pygame.draw.arc(self.__img__, color,
                                [x, y, rad*2, rad*2], pi/2, pi*3/2, 1)
                pygame.draw.arc(self.__img__, color,
                                [x + width - rad*2, y, rad*2, height],
                                pi*3/2, pi/2 + 2*pi, 1)
        else:
            rad = int(width / 2.)
            if rad == 0:
                return
            else:
                pygame.draw.line(self.__img__, color,
                                 (x, y + rad), (x, y + height - rad))
                pygame.draw.line(self.__img__, color, (x + width, y + rad),
                                 (x + width, y + height - rad))
                pygame.draw.arc(self.__img__, color,
                                [x, y, rad*2, rad*2], 0, pi, 1)
                pygame.draw.arc(self.__img__, color,
                                [x, y + height - rad*2, rad*2, rad*2],
                                pi, 2*pi, 1)

    def get_mouse_state(self):
        ''' Get mouse position and states'''

        pos = pygame.mouse.get_pos()
        state = pygame.mouse.get_pressed()

        return (pos, state[0])

    def get_input_key(self):
        ''' Handle key input and send it over to the tracker'''

        ky = []
        for ev in pygame.event.get():
            if ev.type == KEYDOWN:
                keycode = ev.key
                if keycode == K_F1:
                    keycode = pylink.F1_KEY
                elif keycode == K_F2:
                    keycode = pylink.F2_KEY
                elif keycode == K_F3:
                    keycode = pylink.F3_KEY
                elif keycode == K_F4:
                    keycode = pylink.F4_KEY
                elif keycode == K_F5:
                    keycode = pylink.F5_KEY
                elif keycode == K_F6:
                    keycode = pylink.F6_KEY
                elif keycode == K_F7:
                    keycode = pylink.F7_KEY
                elif keycode == K_F8:
                    keycode = pylink.F8_KEY
                elif keycode == K_F9:
                    keycode = pylink.F9_KEY
                elif keycode == K_F10:
                    keycode = pylink.F10_KEY
                elif keycode == K_PAGEUP:
                    keycode = pylink.PAGE_UP
                elif keycode == K_PAGEDOWN:
                    keycode = pylink.PAGE_DOWN
                elif keycode == K_UP:
                    keycode = pylink.CURS_UP
                elif keycode == K_DOWN:
                    keycode = pylink.CURS_DOWN
                elif keycode == K_LEFT:
                    keycode = pylink.CURS_LEFT
                elif keycode == K_RIGHT:
                    keycode = pylink.CURS_RIGHT
                elif keycode == K_BACKSPACE:
                    keycode = ord('\b')
                elif keycode == K_RETURN:
                    keycode = pylink.ENTER_KEY
                elif keycode == K_ESCAPE:
                    keycode = pylink.ESC_KEY
                elif keycode == K_TAB:
                    keycode = ord('\t')
                elif(keycode == pylink.JUNK_KEY):
                    keycode = 0
                else:
                    pass
                ky.append(pylink.KeyInput(keycode, ev.mod))

        return ky

    def exit_image_display(self):
        ''' Exit the camera image display'''

        self.clear_cal_display()

    def alert_printf(self, msg):
        print(msg)

    def setup_image_display(self, width, height):
        ''' Setup the camera image display

        return 1 to request high-resolution camera image'''

        self.size = (width, height)
        self.clear_cal_display()
        self.last_mouse_state = -1

        return 1

    def image_title(self, text):
        ''' Show the camera image title, e.g., target distance,
        and pupil/CR thresholds below the image'''

        txt_w, txt_h = self.fnt.size(text)
        win_w, win_h = self.win.get_size()
        txt_surf = self.fnt.render(text, True, self.fgColor)
        txt_pos = (int((win_w - txt_w)/2),
                   int((win_h + self.size[1])/2 + txt_h))
        # clear the camera title area
        pygame.draw.rect(self.win, self.bgColor,
                         pygame.Rect(0, txt_pos[1], win_w, win_h))
        self.win.blit(txt_surf, txt_pos)  # draw the camera title

    def draw_image_line(self, width, line, totlines, buff):
        ''' Draw the camera image'''

        for i in range(width):
            try:
                self.imagebuffer.append(self.pal[buff[i]])
            except:
                pass

        if line == totlines:
            cam_img = pygame.image.frombuffer(self.imagebuffer.tostring(),
                                              (width, totlines), 'RGBX')
            self.__img__ = cam_img
            self.draw_cross_hair()

            # Scale the image, if needed
            cam_img = pygame.transform.scale(cam_img, self.size)

            # Draw the camera image on screen
            cam_img_pos = ((self.win.get_width()-self.size[0])/2,
                           (self.win.get_height()-self.size[1])/2)
            surf = pygame.display.get_surface()
            surf.blit(cam_img, cam_img_pos)
            # Redraw in the back buffer
            pygame.display.flip()
            surf.blit(cam_img, cam_img_pos)

            self.imagebuffer = array.array('I')

    def set_image_palette(self, r, g, b):
        ''' Get the color palette for the camera image'''

        sz = len(r)
        i = 0
        self.pal = []
        while i < sz:
            rf = int(b[i])
            gf = int(g[i])
            bf = int(r[i])
            self.pal.append((rf << 16) | (gf << 8) | (bf))
            i = i + 1
