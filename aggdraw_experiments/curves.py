#!/usr/bin/env python

# Copy some aggdraw examples from its GitHub repository
# Just to see what they do.

import PIL.Image
from aggdraw import Draw, Pen, Brush, Path

def test_graphics(img):
    draw = Draw(img)

    pen = Pen("red",2)
    brush = Brush("black")

    sp = Path()
    sp.moveto(100,100)
    sp.lineto(100,400)
    sp.lineto(400,400)
    sp.lineto(400,100)
    draw.line(sp, Pen("blue",4))

    cp = Path()
    cp.moveto(100,100)
    cp.curveto(100, 400, 400, 400, 400, 100)
    draw.line(cp, Pen("red",2))

    return draw

img = PIL.Image.new(mode='RGB',size=(500,500),color='grey')
result = test_graphics(img)
result.flush()

img.save("curves.png")
