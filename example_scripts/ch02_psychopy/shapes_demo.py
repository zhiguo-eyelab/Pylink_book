# Filename: shapes_demo.py

from psychopy import visual, event, core

win = visual.Window(size=[800, 600], units='pix')

# line
line_vertices = [(-400,-300), (400,300)] 
line = visual.ShapeStim(win, vertices=line_vertices, lineColor='white', closeShape=False)

# rectangle
rect_vertices = [(-400,-300), (-320,-300), (-320,-240), (-400,-240)]
rect = visual.ShapeStim(win, vertices=rect_vertices, fillColor='blue', lineWidth=0)

# draw a polygon
poly = visual.Polygon(win, edges=6, radius=100, fillColor='green')

while True:
    if rect.overlaps(poly):
        poly.fillColor='red'
    else:
        poly.fillColor='green'
    line.draw()
    poly.draw()
    rect.draw()
    win.flip()
    rect.pos += (4,3) # rectangle moving along the line
    if rect.contains((400,300)):
        break

# quite PsychoPy
win.close()
core.quit()
