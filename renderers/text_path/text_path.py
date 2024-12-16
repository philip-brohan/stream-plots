#!/usr/bin/env python
# Experiments with manipulating text paths

import os
import sys

import numpy as np
from scipy.stats.qmc import PoissonDisk
from Met_palettes import MET_PALETTES
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from scipy.interpolate import splprep, splev, interp1d
from copy import deepcopy


pscale = 10
pwidth = 0
plot_width = 1000 * pscale
plot_height = 500 * pscale
poisson_radius = 0.005 * 1
pen = []
scheme = MET_PALETTES["Signac"]
bgcol = (225, 225, 225)


# Map a path onto a curve [x,y]
def map_path(path, x, y):
    Vx, Vy = path.vertices[:, 0], path.vertices[:, 1]
    dVx = (Vx - np.min(Vx)) / (np.max(Vx) - np.min(Vx))  # map onto 0-1
    dVy = Vy - np.mean(Vy)  # Assume original path is // to x-axis
    # We want to map Vx into distance along the curve
    dx = np.diff(x)
    dy = np.diff(y)
    distancesL = np.sqrt(dx**2 + dy**2)  # Local distance
    distances = np.cumsum(distancesL)  # Integrated distance to point
    # Create a mapping between a uniform 0-1 range and the distance along the curve
    interpolator = interp1d(np.linspace(0, 1, len(distances)), distances)
    # Map the dVx to the distance along the curve
    dVxdist = interpolator(dVx)
    # Create a mapping between the distance along the curve and the curve
    tckC, u = splprep([y, x], s=0)
    # Map the distance along the curve to the curve
    nVy, nVx = splev(dVxdist / np.max(dVxdist), tckC)
    # Get the gradients at the same points
    dy, dx = splev(dVxdist / np.max(dVxdist), tckC, der=1)
    # Calculate the scaling factor - local speed
    interpolator = interp1d(np.linspace(0, 1, len(distancesL)), distancesL)
    dVxspeed = interpolator(dVx)
    print(distancesL[:100])
    print(dVxspeed[:100])
    dVxspeed = dVxspeed / np.mean(dVxspeed)
    # Generate the mapped-path vertices
    tan_g = dy / dx
    dscale = 1 / dVxspeed
    ndVx = -dVy * dscale * tan_g / np.sqrt(1 + tan_g**2)
    ndVy = dVy * dscale / np.sqrt(1 + tan_g**2)
    nVx = nVx + ndVx
    nVy = nVy + ndVy
    # Make the new path with these vertices
    new_path = deepcopy(path)
    new_path.vertices[:, 0] = nVx
    new_path.vertices[:, 1] = nVy
    return new_path


# Make the plot
fig = Figure(
    figsize=(38.4, 21.6),  # Width, Height (inches)
    dpi=100,
    facecolor=(0.9, 0.9, 0.9, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=True,
    subplotpars=None,
    tight_layout=None,
)
# Attach a canvas
canvas = FigureCanvas(fig)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()  # Don't want surrounding x and y axis
ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)
ax.set_aspect("auto")

opath = TextPath(
    (-150, 0),
    "The seven heavenly virtues are prudence, justice, temperance, courage, faith, hope, and love.",
    size=6,
    prop="Serif",
)
opatch = PathPatch(
    opath, facecolor=(1, 0, 0, 1), edgecolor=None, linewidth=0, zorder=20
)
ax.add_artist(opatch)
Vx, Vy = opath.vertices[:, 0], opath.vertices[:, 1]
# ax.add_line(Line2D(Vx, Vy, color="black", linewidth=1, zorder=10))

# Create a curve to map the path onto
x = np.linspace(0, 1, 100) * np.linspace(1, 2, 100)
x = x / 2 * 180 - 90
y = np.sin(4 * x * np.pi / 180) * 45

# x = np.linspace(0, 1, 100) * np.linspace(1, 2, 100) * 180 - 90 - 45
# y = np.linspace(0, 1, 100) * np.linspace(1, 2, 100) * 90 - 45 - 25

npath = map_path(opath, x, y)
npatch = PathPatch(
    npath, facecolor=(0, 0, 1, 1), edgecolor=None, linewidth=0, zorder=20
)
ax.add_artist(npatch)
Vx, Vy = npath.vertices[:, 0], npath.vertices[:, 1]
# ax.add_line(Line2D(Vx, Vy, color="black", linewidth=1, zorder=10))

fig.savefig("text_path.webp")
