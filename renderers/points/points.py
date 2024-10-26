#!/usr/bin/env python

# Plot a random (poisson disk) set of points
import numpy as np
import PIL.Image
from aggdraw import Draw, Pen, Brush
from scipy.stats.qmc import PoissonDisk

from Met_palettes import MET_PALETTES

plot_width = 1024
plot_height = 1024
poisson_radius = 0.005 * 1.5

# Generate a set of origin points for the wind vectors
engine = PoissonDisk(d=2, radius=poisson_radius)
points = engine.fill_space()
points = points * max(plot_width, plot_height)
points = points[(points[:, 1] < plot_height) & (points[:, 0] < plot_width)]


# Render the points
def render_points(img, points, pen, brush, size=10):
    draw = Draw(img)

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
colours = MET_PALETTES["Hokusai2"]["colors"]
for colour in colours:
    pen.append(Pen(colour, 1))
    brush.append(
        Brush(
            colour,
        )
    )
bgcol = (225, 225, 225)
img = PIL.Image.new(mode="RGB", size=(plot_width, plot_height), color=bgcol)

result = render_points(
    img,
    points,
    pen,
    brush,
)
result.flush()

img.save("points.webp")
