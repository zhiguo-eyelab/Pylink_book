#Filename: text_demo.py

import pygame, sys
pygame.init()

# open a window
win = pygame.display.set_mode((300,200))

# create a font object and enable 'underline'
fnt = pygame.font.SysFont('arial', 32, bold=True, italic=True)
fnt.set_underline(True)

# size() estimates the width and height of the rendered text surface
w, h = fnt.size('Hello, World!')
print(w,h)

# render the text to get a surface
win.fill((0, 0, 0))
text_surf = fnt.render('Hello, World!', True, (255,0,0))

# show(blit) the text surface at the window center
win.blit(text_surf, (150-w/2,100-h/2))
pygame.display.flip()

# show the text until a key is pressed
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.KEYUP: 
            pygame.quit()
            sys.exit()
