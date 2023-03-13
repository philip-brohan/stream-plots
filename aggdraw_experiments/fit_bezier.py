#!/usr/bin/env python

# Plot a bezier curve fitted to a sequence of points

import PIL.Image
import numpy as np
from aggdraw import Draw, Pen, Brush, Path

def get_bezier_coef(points):
    # since the formulas work given that we have n+1 points
    # then n must be this:
    n = len(points) - 1
    # build coefficents matrix
    C = 4 * np.identity(n)
    np.fill_diagonal(C[1:], 1)
    np.fill_diagonal(C[:, 1:], 1)
    C[0, 0] = 2
    C[n - 1, n - 1] = 7
    C[n - 1, n - 2] = 2
    # build points vector
    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
    P[0] = points[0] + 2 * points[1]
    P[n - 1] = 8 * points[n - 1] + points[n]
    # solve system, find a & b
    A = np.linalg.solve(C, P)
    B = [0] * n
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2
    return A, B

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
    points = np.empty((4,2))
    points[0]=[100,100]                                                                                                                             
    points[1]=[100,400]                                                                                                                             
    points[2]=[400,400]                                                    
    points[3]=[400,100]                                                    
    (x,y) = get_bezier_coef(points)
    cp.curveto(int(x[0,0]),int(x[0,1]),int(y[0][0]),int(y[0][1]),int(points[1,0]),int(points[1,1]))
    cp.curveto(int(x[1,0]),int(x[1,1]),int(y[1][0]),int(y[1][1]),int(points[2,0]),int(points[2,1]))
    cp.curveto(int(x[2,0]),int(x[2,1]),int(y[2][0]),int(y[2][1]),int(points[3,0]),int(points[3,1]))
    draw.line(cp, Pen("red",2))

    return draw

img = PIL.Image.new(mode='RGB',size=(500,500),color='grey')
result = test_graphics(img)
result.flush()

img.save("fit_bezier.png")
