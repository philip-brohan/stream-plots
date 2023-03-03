#!/usr/bin/env python

# Copy some aggdraw examples from its GitHub repository
# Just to see hat they do.

import PIL.Image
from aggdraw import Draw, Pen, Brush, Symbol

def test_graphics(img):
    draw = Draw(img)

    pen = Pen("red",1)
    brush = Brush("black")

    draw.symbol((0, 0),Symbol("M0,0L0,0L0,0L0,0Z"), pen)
    draw.symbol((0, 0),Symbol("M0,0L0,0,0,0,0,0Z", 10), pen)
    draw.symbol((0, 0),Symbol("M0,0C0,0,0,0,0,0Z"), pen)
    draw.symbol((0, 0),Symbol("M0,0S0,0,0,0,0,0Z"), pen)
    Symbol()

    draw.symbol((0, 0),Symbol("m0,0l0,0l0,0l0,0z"), pen)
    draw.symbol((0, 0),Symbol("m0,0l0,0,0,0,0,0z", 10), pen)
    draw.symbol((0, 0),Symbol("m0,0c0,0,0,0,0,0z"), pen)
    draw.symbol((0, 0),Symbol("m0,0s0,0,0,0,0,0z"), pen)

    symbol = Symbol("M400 200 L400 400")
    draw.symbol((0, 0), symbol, pen)

    return draw

img = PIL.Image.new(mode='RGB',size=(500,500),color='white')
result = test_graphics(img)
result.flush()

img.save("symbol.png")
