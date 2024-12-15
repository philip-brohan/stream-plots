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
from matplotlib.transforms import Affine2D
from scipy.interpolate import make_interp_spline
from scipy.interpolate import splprep, splev
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
    # path = TextPath((-90, 0), "Test string of reasonable length", size=4, prop="Serif")
    # curve = np.linspace(0, 1, 100)
    Vx, Vy = path.vertices[:, 0], path.vertices[:, 1]
    dVx = (Vx - np.min(Vx)) / (np.max(Vx) - np.min(Vx))  # map onto 0-1
    dVy = Vy - np.mean(Vy)  # Assume original path is // to x-axis
    # We want to map Vx into distance along the curve, and Vy into distance perpendicular to the curve.
    dx = np.diff(x)
    dy = np.diff(y)
    distances = np.sqrt(dx**2 + dy**2)
    distances = np.cumsum(distances)
    distances = np.insert(distances, 0, 0)
    tck, u = splprep([np.linspace(0, 1, len(distances)), distances], s=0)
    disc, ddist = splev(dVx, tck)  # Distance along curve
    tck, u = splprep([x, y], s=0)
    nVxl, nVyl = splev(ddist / np.max(ddist), tck)  # Vertex points along curve
    nVx = nVxl
    nVy = nVyl + dVy
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
    (-90, 0),
    "The seven heavenly virtues are prudence, justice, temperance, courage, faith, hope, and love.",
    size=4,
    prop="Serif",
)
opatch = PathPatch(
    opath, facecolor=(1, 0, 0, 0.5), edgecolor=None, linewidth=0, zorder=20
)
ax.add_artist(opatch)
Vx, Vy = opath.vertices[:, 0], opath.vertices[:, 1]
ax.add_line(Line2D(Vx, Vy, color="black", linewidth=1, zorder=10))

# Create a curve to map the path onto
x = np.linspace(-90, 90, 100)
y = np.linspace(-45, 45, 100)

npath = map_path(opath, x, y)
npatch = PathPatch(
    npath, facecolor=(0, 0, 1, 0.5), edgecolor=None, linewidth=0, zorder=20
)
ax.add_artist(npatch)
Vx, Vy = npath.vertices[:, 0], npath.vertices[:, 1]
ax.add_line(Line2D(Vx, Vy, color="black", linewidth=1, zorder=10))

fig.savefig("text_path.webp")
