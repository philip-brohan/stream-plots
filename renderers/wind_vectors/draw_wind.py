#!/usr/bin/env python
# Wind vector plot - for custom wind field.
# Plots anti-aliased vectors rather than advecting points.

import os
import sys
import numpy as np
import PIL.Image
from aggdraw import Draw, Pen
from scipy.stats.qmc import PoissonDisk

from utils.colours import colourSets

pscale = 1
pwidth = 1
plot_width = 1024 * pscale
plot_height = 1024 * pscale
iterations = 50
epsilon = 0.05 / 2
poisson_radius = 0.005 * 3
pen = []
colours = colourSets["RYBBW"]
for colour in colours:
    pen.append(Pen(colour, 20 * pscale * pwidth))
bgcol = (225, 225, 225)
penb = Pen(bgcol, 30 * pscale * pwidth)
data_resolution = 0.2


u = np.zeros([plot_width, plot_height])
v = u.copy()


# Add a cyclone (circular wind field)
def add_cyclone(u, v, x, y, strength=10, decay=0.1):
    lats = range(plot_height)
    lons = range(plot_width)
    lons_g, lats_g = np.meshgrid(lons, lats)
    rsq = (lons_g - x) ** 2 + (lats_g - y) ** 2
    rsq[rsq < 1] = 1
    tx = 1 * (lats_g - y) / rsq
    ty = 1 * (lons_g - x) / rsq
    speed = strength / (1.0 + rsq * decay)
    u += speed * tx
    v += speed * ty
    return (u, v)


for ci in range(10):
    cyclone = [
        np.random.random() * plot_width,
        np.random.random() * plot_height,
        np.random.random() * 200 - 100,
        0.000001,
    ]
    u10m, v10m = add_cyclone(
        u, v, cyclone[0], cyclone[1], strength=cyclone[2], decay=cyclone[3]
    )
u += 2  # 2
speed = np.sqrt(u**2 + v**2)
min_speed = 0.75
max_speed = 3
v[speed < min_speed] *= min_speed / v[speed < min_speed]
u[speed < min_speed] *= min_speed / u[speed < min_speed]
v[speed > max_speed] *= max_speed / speed[speed > max_speed]
u[speed > max_speed] *= max_speed / speed[speed > max_speed]

# Generate a set of origin points for the wind vectors
engine = PoissonDisk(d=2, radius=poisson_radius)
sample = engine.fill_space()
sample = sample * max(plot_width, plot_height)
sample = sample[(sample[:, 1] < plot_height) & (sample[:, 0] < plot_width)]
opx = sample[:, 0]
opy = sample[:, 1]

# Each point in this field has an index location (i,j)
#  and a real (x,y) position
xc = list(range(plot_width))
xmin = np.min(xc)
xmax = np.max(xc)
dwidth = len(xc)
yc = list(range(plot_height))
ymin = np.min(yc)
ymax = np.max(yc)
dheight = len(yc)


# Convert between index and real positions
def x_to_i(x, width):
    return np.minimum(
        width - 1, np.maximum(0, np.floor((x - xmin) / (xmax - xmin) * (width - 1)))
    ).astype(int)


def y_to_j(y, height):
    return np.minimum(
        height - 1,
        np.maximum(0, np.floor((y - ymin) / (ymax - ymin) * (height - 1))),
    ).astype(int)


# Propagate the origin points with the wind
def wind_vectors(uw, vw, opx, opy, iterations=5, epsilon=1):
    op = np.empty((len(opx), 2, iterations + 1))
    op[:, 0, 0] = opx
    op[:, 1, 0] = opy
    # Repeatedly make a new set of x,y points by moving the previous set with the wind
    for k in range(iterations):
        i = x_to_i(op[:, 0, k], dwidth)
        j = y_to_j(op[:, 1, k], dheight)
        op[:, 0, k + 1] = op[:, 0, k] + epsilon * uw[j, i]
        op[:, 0, k + 1][op[:, 0, k + 1] > xmax] = xmax
        op[:, 0, k + 1][op[:, 0, k + 1] < xmin] = xmin
        op[:, 1, k + 1] = op[:, 1, k] + epsilon * vw[j, i]
        op[:, 1, k + 1][op[:, 1, k + 1] > ymax] = ymax
        op[:, 1, k + 1][op[:, 1, k + 1] < ymin] = ymin
    return op


line_points = wind_vectors(
    u,
    v,
    opx,
    opy,
    epsilon=epsilon,
    iterations=iterations,
)


def render_lines(img, op, pen, penb=None):
    draw = Draw(img)

    lp = np.empty(((iterations + 1) * 2))
    for line in range(op.shape[0]):
        lp[0::2] = x_to_i(op[line, 0, :], plot_width)
        lp[1::2] = y_to_j(op[line, 1, :], plot_height)
        if penb is not None:
            draw.line(lp, penb)
        pl = pen[line % len(pen)]
        draw.line(lp, pl)
    return draw


img = PIL.Image.new(mode="RGB", size=(plot_width, plot_height), color=bgcol)
result = render_lines(img, line_points, pen, penb=penb)
result.flush()

img.save("wind_lines.png")
