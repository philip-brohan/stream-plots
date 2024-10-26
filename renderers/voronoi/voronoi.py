#!/usr/bin/env python

# Plot a voronoi map of a random (poisson disk) set of points
import sys
import numpy as np
import PIL.Image
from aggdraw import Draw, Pen, Brush
from scipy.stats.qmc import PoissonDisk
from scipy.spatial import Voronoi

from Met_palettes import MET_PALETTES

plot_width = 1024
plot_height = 1024
poisson_radius = 0.005 * 4

# Generate a set of origin points
engine = PoissonDisk(d=2, radius=poisson_radius)
points = engine.fill_space()
points = points * max(plot_width, plot_height)
points = points[(points[:, 1] < plot_height) & (points[:, 0] < plot_width)]

# Make the voronoi polyhedra
vor = Voronoi(points)

# List the neighbours associated with each point
neighboursForPoint = [[] for _ in range(len(vor.points))]
for ridge in vor.ridge_points:
    neighboursForPoint[ridge[0]].append(ridge[1])
    neighboursForPoint[ridge[1]].append(ridge[0])

# Actually want the colours of the neighbours
# So make a list of the colour index used for each point
coloursForPoint = [None for _ in range(len(vor.points))]


# Don't want two regions that share a boundary in the same colour
def getBlockedColours(pointI):
    Blocked = []
    for npointI in neighboursForPoint[pointI]:
        if coloursForPoint[npointI] is not None:
            Blocked.append(coloursForPoint[npointI])
    return Blocked


# Render the regions
def render_regions(img, vor, pen, brush, size=25):
    draw = Draw(img)

    for pointI in range(len(vor.points)):
        cIdx = None
        vertices = []
        blockedColours = getBlockedColours(pointI)
        region = vor.point_region[pointI]
        if region == -1:  # Outside image
            continue
        for vertexI in vor.regions[region]:
            if vertexI < 0:  # Outside image
                vertices = []
                break
            vertices.extend(vor.vertices[vertexI])
            for cIi in range(len(pen)):
                if cIi not in blockedColours:
                    cIdx = cIi
                    break
        if len(vertices) == 0:
            continue
        if cIdx is None:
            continue
        pl = pen[cIdx]
        bl = brush[cIdx]
        draw.polygon(vertices, pl, bl)
        coloursForPoint[pointI] = cIdx
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

result = render_regions(
    img,
    vor,
    pen,
    brush,
)
result.flush()


img.save("voronoi.webp")
