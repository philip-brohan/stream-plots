#!/usr/bin/env python

# Copy some aggdraw examples from its GitHub repository
# Just to see what they do.

import PIL.Image
from aggdraw import Draw, Pen, Brush

def test_graphics(img):
    draw = Draw(img)

    pen = Pen("red",10)
    brush = Brush("black")

    draw.line((50, 50, 100, 100), pen)

    draw.rectangle((50, 150, 100, 200), pen)
    draw.rectangle((50, 220, 100, 270), brush)
    draw.rectangle((50, 290, 100, 340), brush, pen)
    draw.rectangle((50, 360, 100, 410), Pen("Blue",5), brush)

    draw.ellipse((120, 150, 170, 200), pen)
    draw.ellipse((120, 220, 170, 270), brush)
    draw.ellipse((120, 290, 170, 340), brush, pen)
    draw.ellipse((120, 360, 170, 410), pen, brush)

    draw.polygon((190+25, 150, 190, 200, 190+50, 200), pen)
    draw.polygon((190+25, 220, 190, 270, 190+50, 270), brush)
    draw.polygon((190+25, 290, 190, 340, 190+50, 340), brush, pen)
    draw.polygon((190+25, 360, 190, 410, 190+50, 410), pen, brush)

    return draw

img = PIL.Image.new(mode='RGB',size=(500,500),color='white')
result = test_graphics(img)
result.flush()

img.save("brush+pen.png")
