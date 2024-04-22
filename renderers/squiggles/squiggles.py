#!/usr/bin/env python

# Plot random squiggles - long single curved lines

import numpy as np
import PIL.Image
from aggdraw import Draw, Pen, Brush
from scipy.stats.qmc import PoissonDisk

from utils.colours import colourSets

plot_width = 1024
plot_height = 1024
bgcol = (225, 225, 225)
img = PIL.Image.new(mode="RGB", size=(plot_width, plot_height), color=bgcol)
draw = Draw(img)

# Fit a cubic bezier curve to a given set of points
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


# Render a squiggle
def squiggle(draw, pen, start, scale, length)):
    
    def getOffset():
        return (np.random.random() * plot_width*scale, np.random.random() * plot_height*scale)

    points = np.empty((length+1, 2))
    points[0] = start
    for i in range(length):
        points[i+1] = points[i] + getOffset()

    for pointI in range(points.shape[0]):
        pl = pen[pointI % len(pen)]
        bl = brush[pointI % len(brush)]
        draw.ellipse(
            (
                points[pointI, 0] - size / 2,
                points[pointI, 1] - size / 2,
                points[pointI, 0] + size / 2,
                points[pointI, 1] + size / 2,
            ),
            pl,
            bl,
        )
    return draw


pen = []
brush = []
colours = colourSets["Austria"]
for colour in colours:
    pen.append(Pen(colour, 1))
    brush.append(
        Brush(
            colour,
        )
    )

result = render_points(
    img,
    points,
    pen,
    brush,
)
result.flush()

img.save("squiggles.webp")
