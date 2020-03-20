# Filename: EyeLinkCoreGraphicsPyGame.py

import pygame
from pygame.locals import *
from math import pi
import array
import pylink
    
class EyeLinkCoreGraphicsPyGame(pylink.EyeLinkCustomDisplay):
    def __init__(self, tracker, win):
        pylink.EyeLinkCustomDisplay.__init__(self)

        # calibration color, calibration target size, and warning beep
        self.backgroundColor = (128, 128, 128)
        self.foregroundColor = (0,0,0)
        self.targetSize = 32 # diameter of the target circle
        self.enableBeep = True # whether we should play warning beeps

        # screen to use for calibration
        self.win = win
        # set up the tracker
        self.tracker = tracker
            
        # warning beeps
        self.__target_beep__ = pygame.mixer.Sound("type.wav")
        self.__target_beep__done__ = pygame.mixer.Sound("qbeep.wav")
        self.__target_beep__error__ = pygame.mixer.Sound("error.wav")
        
        # initialize some variables for later use
        self.imagebuffer = array.array('I') # buffer for camera image
        self.pal = [] # image palatte, with which the index will be used for drawing
        self.size = [384, 320] # size of the camera image
        self.fnt = pygame.font.SysFont('Arial', 20) # we will use this for text messages
        self.last_mouse_state = -1 # mouse status
        self.img_SF = 1 # enlarge the camera image for displaying
    
    def setup_cal_display (self):
        self.win.fill(self.backgroundColor)
        pygame.display.flip()
        
    def exit_cal_display(self): 
        self.clear_cal_display()

    def record_abort_hide(self):
        pass

    def clear_cal_display(self): 
        self.win.fill(self.backgroundColor)

    def erase_cal_target(self):
        self.win.fill(self.backgroundColor)
        pygame.display.flip()
        
    def draw_cal_target(self, x, y):
        ''' draw the calibration target, i.e., a bull's eye'''
        
        pygame.draw.circle(self.win, self.foregroundColor, (x,y), int(self.targetSize/2.))
        pygame.draw.circle(self.win, self.backgroundColor, (x,y), int(self.targetSize/4.))        
        pygame.display.flip()
        
    def play_beep(self, beepid):
        '''play warning beeps if being requested'''
        
        if not self.enableBeep:
            pass
        else:
            if beepid == pylink.DC_TARG_BEEP or beepid == pylink.CAL_TARG_BEEP:
                self.__target_beep__.play()
            elif beepid == pylink.CAL_ERR_BEEP or beepid == pylink.DC_ERR_BEEP:
                self.__target_beep__error__.play()
            else:#  CAL_GOOD_BEEP or DC_GOOD_BEEP
                self.__target_beep__done__.play()
        
    def getColorFromIndex(self, colorindex):
        ''' color scheme for different elements '''
        
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
        ''' draw lines'''

        color = self.getColorFromIndex(colorindex)

        # the old API assumes a camera image of 192 x 160 pixel
        # the following conversion will fix that 
        w,h = self.__img__.get_size()
        x1 = int(x1*1.0/self.size[0] * w)
        x2 = int(x2*1.0/self.size[0] * w)
        y1 = int(y1*1.0/self.size[1] * h)
        y2 = int(y2*1.0/self.size[1] * h)
        if True not in [i <0 for i in [x1, y1, x2, y2]]:
            pygame.draw.line(self.__img__, color, (x1, y1), (x2, y2))

    def draw_lozenge(self, x, y, width, height, colorindex):
        ''' draw the search limits with two lines and two arcs'''
        
        color = self.getColorFromIndex(colorindex)
        
        w,h = self.__img__.get_size()
        x = int(x/ self.size[0] * w)
        width = int(width/ self.size[0]* w)
        y = int(y/ self.size[1] * h)
        height = int(height / self.size[1] * h)
        if width > height:
            rad = int(height / 2.)
            if rad == 0:
                return
            else:
                pygame.draw.line(self.__img__, color, (x + rad, y), (x + width - rad, y))
                pygame.draw.line(self.__img__, color, (x + rad, y + height), (x + width - rad, y + height))
                pygame.draw.arc(self.__img__, color,[x, y, rad*2, rad*2], pi/2, pi*3/2, 1)
                pygame.draw.arc(self.__img__, color,[x+width-rad*2, y, rad*2, height], pi*3/2, pi/2 + 2*pi, 1)
        else:
            rad = int(width / 2.)
            if rad == 0:
                return
            else:
                pygame.draw.line(self.__img__, color, (x, y + rad), (x, y + height - rad))
                pygame.draw.line(self.__img__, color, (x + width, y + rad), (x + width, y + height - rad))
                pygame.draw.arc(self.__img__, color,[x, y, rad*2, rad*2], 0, pi, 1)
                pygame.draw.arc(self.__img__, color,[x, y+height-rad*2, rad*2, rad*2], pi, 2*pi, 1)

    def get_mouse_state(self):
        ''' get mouse position and states'''
        
        pos = pygame.mouse.get_pos()
        pos = (int(pos[0]*1.0/self.win.get_width()*self.size[0]),
               int(pos[1]*1.0/self.win.get_height()*self.size[1]))
        
        state = pygame.mouse.get_pressed()
        return (pos, state[0])
    
    def get_input_key(self):
        ''' handle key input and send it over to the tracker'''
        
        ky = []
        for ev in pygame.event.get():
            if ev.type != KEYDOWN:
                pass
            else:
                keycode = ev.key
                if keycode == K_F1:  keycode = pylink.F1_KEY
                elif keycode == K_F2:  keycode = pylink.F2_KEY
                elif keycode == K_F3:  keycode = pylink.F3_KEY
                elif keycode == K_F4:  keycode = pylink.F4_KEY
                elif keycode == K_F5:  keycode = pylink.F5_KEY
                elif keycode == K_F6:  keycode = pylink.F6_KEY
                elif keycode == K_F7:  keycode = pylink.F7_KEY
                elif keycode == K_F8:  keycode = pylink.F8_KEY
                elif keycode == K_F9:  keycode = pylink.F9_KEY
                elif keycode == K_F10: keycode = pylink.F10_KEY

                elif keycode == K_PAGEUP: keycode = pylink.PAGE_UP
                elif keycode == K_PAGEDOWN:  keycode = pylink.PAGE_DOWN
                elif keycode == K_UP:   keycode = pylink.CURS_UP
                elif keycode == K_DOWN:  keycode = pylink.CURS_DOWN
                elif keycode == K_LEFT:  keycode = pylink.CURS_LEFT
                elif keycode == K_RIGHT: keycode = pylink.CURS_RIGHT

                elif keycode == K_BACKSPACE:    keycode = ord('\b')
                elif keycode == K_RETURN:  keycode = pylink.ENTER_KEY
                elif keycode == K_ESCAPE:  keycode = pylink.ESC_KEY
                elif keycode == K_TAB:   keycode = ord('\t')
                elif(keycode == pylink.JUNK_KEY): keycode = 0
                
                ky.append(pylink.KeyInput(keycode, ev.mod))
        return ky
        
    def exit_image_display(self):
        self.clear_cal_display()
        pygame.display.flip()
        
    def alert_printf(self, msg): 
        print(msg)
            
    def setup_image_display(self, width, height):
        self.clear_cal_display()
        self.last_mouse_state = -1
        
    def image_title(self, text):
        ''' show pupil CR thresholds below the image'''
        
        txt_w, txt_h = self.fnt.size(text)
        win_w, win_h = self.win.get_size()
        cam_w, cam_h = self.size
        txt_surf = self.fnt.render(text, True, self.foregroundColor)
        txt_pos = (int((win_w - txt_w)/2),int((win_h + cam_h*self.img_SF)/2 + txt_h))
        # we need to clear the text area first
        pygame.draw.rect(self.win, self.backgroundColor, pygame.Rect((0, txt_pos[1]), (win_w, txt_h)))
        self.win.blit(txt_surf, txt_pos)
        pygame.display.flip()
        # redraw in the back buffer
        pygame.draw.rect(self.win, self.backgroundColor, pygame.Rect((0, txt_pos[1]), (win_w, txt_h)))
        self.win.blit(txt_surf, txt_pos)
        
    def draw_image_line(self, width, line, totlines, buff):         
        ''' draw the camera image'''

        self.size = [width, totlines] # update the size of camera image
        # clear the image buffer when a new image comes in, i.e., line ==1
        if line == 1:
            self.imagebuffer = array.array('I')

        if totlines < 320:
            self.img_SF = 2
        else:
            self.img_SF = 1

        for i in range(width):
            try:
                self.imagebuffer.append(self.pal[buff[i]])
            except:
                pass
            
        if line == totlines:
            self.__img__ = pygame.image.frombuffer(self.imagebuffer, (width, totlines), 'RGBX')
            self.draw_cross_hair()
            cam_img = pygame.transform.scale(self.__img__, (width*self.img_SF,
                                                            totlines*self.img_SF))
            self.__img__ = None
            cam_img_pos = ((self.win.get_width()-cam_img.get_width())/2,
                           (self.win.get_height()-cam_img.get_height())/2)
            self.win.blit(cam_img, cam_img_pos)
            pygame.display.flip()
            # redraw in the back buffer
            self.win.blit(cam_img, cam_img_pos)
            self.imagebuffer = array.array('I')
            
    def set_image_palette(self, r, g, b):
        ''' get the color palette for the camera image'''
        
        sz = len(r)
        i = 0
        self.pal = []
        while i < sz:
            rf = int(b[i])
            gf = int(g[i])
            bf = int(r[i])
            self.pal.append((rf << 16) | (gf << 8) | (bf))
            i = i + 1
