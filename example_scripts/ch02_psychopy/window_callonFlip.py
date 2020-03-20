# Filename: window_callonFlip.py

from psychopy import visual, core

win = visual.Window(size=[800,600], units="pix")

# define a dummy TTL triggering function
def send_ttl(code):
    current_t = core.getTime()
    print('TTL-%d being sent at time: %d' % (code, current_t))
    
for ttl in range(101, 105):
    win.callOnFlip(send_ttl, ttl)
    flip_t = win.flip()
    print('Actual flipping time: %d'%flip_t)
    core.wait(1.0)

# quit PsychoPy
win.close()
core.quit()