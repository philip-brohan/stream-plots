#!/usr/bin/env python

# Plot a wind field using text strings from the shipping forecast

import os
import sys
import iris
import iris.coords
import iris.coord_systems
import iris.fileformats
import iris.util

iris.FUTURE.datum_support = True  # I don't care about datums
import numpy as np
from scipy.stats.qmc import PoissonDisk
from Met_palettes import MET_PALETTES
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import PathPatch
from copy import deepcopy
from datetime import datetime

import random

from cube import plot_cube
from streamlines import wind_vectors
from textPath import map_path, string_to_path, curve_length, path_length, trim_curve
from collisions import collision_check, collision_cut

# Parameters
plot_width = 3200
plot_height = 2100
plot_x = [-18.3 / 0.6, 3 / 0.6]  # plot range lat & lon
plot_y = [48, 62]
data_x = [-22.5 / 0.6, 8 / 0.6]
data_y = [43, 67]
data_resolution = 0.05  # degrees (units of u wind)
collision_resolution = 0.05  # same
# Cube for the wind field
data_cube = plot_cube(
    data_resolution, xmin=data_x[0], xmax=data_x[1], ymin=data_y[0], ymax=data_y[1]
)
# Cube for the collision detection
collision_cube = plot_cube(
    collision_resolution, xmin=data_x[0], xmax=data_x[1], ymin=data_y[0], ymax=data_y[1]
)
collision_cube.data = np.zeros(collision_cube.data.shape)

iterations = 250 * 4  # How far the streamlines propagate (max)
epsilon = 0.005 / 4

poisson_radius = 0.005  # Figure fraction - separation of streamline start points

scheme = MET_PALETTES["Hokusai2"]
bgcol = (1, 1, 0.95, 1)  # "#ffe6b7"  # (255 / 255, 255 / 255, 255 / 255, 1.0)

font_size = 0.35  # Scaling for the TextPath - 4 is about right to match the degrees
fprop = "Serif"  # font choice

# Load the land mask
land_mask = iris.load_cube(
    "%s/fixed_fields/land_mask/opfc_global_2019.nc" % os.getenv("DATADIR")
)
land_mask = land_mask.regrid(data_cube, iris.analysis.Linear())

# Load the wind field
fctime = datetime(2024, 12, 7, 6)
vwnd = iris.load_cube(
    "%s/opfc/glm/2024/12/07.pp" % os.getenv("SCRATCH"),
    iris.AttributeConstraint(STASH=iris.fileformats.pp.STASH(1, 3, 226))
    & iris.Constraint(forecast_period=0)
    & iris.Constraint(forecast_reference_time=fctime),
)
uwnd = iris.load_cube(
    "%s/opfc/glm/2024/12/07.pp" % os.getenv("SCRATCH"),
    iris.AttributeConstraint(STASH=iris.fileformats.pp.STASH(1, 3, 225))
    & iris.Constraint(forecast_period=0)
    & iris.Constraint(forecast_reference_time=fctime),
)
u10m = uwnd.regrid(data_cube, iris.analysis.Linear())
# iris.save(u10m, "u10m.nc")
v10m = vwnd.regrid(data_cube, iris.analysis.Linear())
# v10m.data *= -1  # Want +ve going north
# iris.save(v10m, "v10m.nc")

# Load the shipping forecast
with open("./forecast_20241207.txt", "r") as file:
    # Read all lines into a list of strings
    lines = file.readlines()

# Remove blank lines from the list
lines = [line.strip() for line in lines if line.strip()]

# Strip out the lines with assigned start points
alines = [line for line in lines if line.startswith("[")]
lines = [line for line in lines if not line.startswith("[")]


# Find longest line shorter than some given curve
def line_shorter_than(linePaths, x, y):
    max_length = curve_length(x, y)
    short_line = None
    for line in linePaths:
        pl = path_length(linePaths[line])
        if pl < max_length:
            if short_line is None or pl > path_length(linePaths[short_line]):
                short_line = line
    return short_line


# Set up the plot
fig = Figure(
    figsize=(int(plot_width / 100), int(plot_height / 100)),
    dpi=100,
    facecolor=bgcol,
    edgecolor=None,
    linewidth=0.0,
    frameon=True,
    subplotpars=None,
    tight_layout=None,
)
canvas = FigureCanvas(fig)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()  # Don't want surrounding x and y axis
ax.set_xlim(plot_x[0], plot_x[1])
ax.set_ylim(plot_y[0], plot_y[1])
ax.set_aspect("auto")

# Add the assigned lines
for line in alines:
    udx = line.find(",")
    x = float(line[1:udx])
    udx2 = line.find(",", udx + 1)
    y = float(line[udx + 1 : udx2])
    udx3 = line.find("]", udx2 + 1)
    fonts = float(line[udx2 + 1 : udx3])
    line = line[udx3 + 1 :]
    wv = wind_vectors(
        u10m,
        v10m,
        np.array([x]),
        np.array([y]),
        epsilon=epsilon,
        iterations=iterations * 2,
    )
    lp = string_to_path(line, fsize=fonts, fprop=fprop, sy=1)
    npath = map_path(lp, wv[0, 0, :], wv[0, 1, :])
    npatch = PathPatch(
        npath,
        facecolor="red",
        edgecolor="black",
        linewidth=0.25,
        zorder=30,
    )
    npatch2 = PathPatch(
        npath,
        facecolor="red",
        edgecolor="black",
        linewidth=0.25,
        alpha=0.25,
        zorder=80,
    )
    ax.add_artist(npatch)
    ax.add_artist(npatch2)
    collision_check(collision_cube, npath.vertices[:, 0], npath.vertices[:, 1])

if True:
    # Generate a set of origin points for the text strings
    engine = PoissonDisk(d=2, radius=poisson_radius)
    sample = engine.fill_space()
    sample = sample * (data_x[1] - data_x[0])
    sample[:, 0] += data_x[0]
    sample[:, 1] += data_y[0]
    sample = sample[(sample[:, 1] > data_y[0]) & (sample[:, 1] < data_y[1])]
    wpx = sample[:, 0]
    wpy = sample[:, 1]

    text_points = wind_vectors(
        u10m,
        v10m,
        wpx,
        wpy,
        epsilon=epsilon,
        iterations=iterations,
    )

    count = 0
    for fontSize in [0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2]:
        # # Add the streamlines in random order
        line_sequence = random.sample(
            list(range(text_points.shape[0])), text_points.shape[0]
        )
        # Make a TextPath for each line (to get the size)
        linePaths = {}
        for line in lines:
            linePaths[line] = string_to_path(line, fsize=fontSize, fprop=fprop, sy=1)
        olinePaths = deepcopy(linePaths)

        for streamline in line_sequence:
            try:
                x = text_points[streamline, 0, :].copy()
                y = text_points[streamline, 1, :].copy()
                x, y = collision_cut(collision_cube, x, y)
                short_line = line_shorter_than(linePaths, x, y)
                if short_line is None:
                    continue
                # random_line = random.choice(short_lines)
                x, y = trim_curve(x, y, path_length(linePaths[short_line]))
                if len(x) < 4:  # Too short - try again
                    print("short x")
                    continue
                npath = map_path(linePaths[short_line], x, y)
                fcol = facecolor = scheme["colors"][count % len(scheme["colors"])]
                npatch = PathPatch(
                    npath,
                    facecolor=fcol,
                    edgecolor="black",
                    linewidth=0.25,
                    zorder=30,
                )
                npatch2 = PathPatch(
                    npath,
                    facecolor=fcol,
                    edgecolor="black",
                    linewidth=0.25,
                    alpha=0.25,
                    zorder=80,
                )
                if not collision_check(
                    collision_cube, npath.vertices[:, 0], npath.vertices[:, 1]
                ):
                    ax.add_artist(npatch)
                    ax.add_artist(npatch2)
                    count += 1
                    # del linePaths[random_line]
                    line_sequence.remove(streamline)
                    if len(linePaths) == 0:
                        linePaths = deepcopy(olinePaths)
                    continue
            except Exception as e:
                print(e)
                continue

# Add the land mask - temporary addition
lats = land_mask.coord("latitude").points
lons = land_mask.coord("longitude").points
mask_img = ax.pcolorfast(
    lons,
    lats,
    land_mask.data,
    cmap=matplotlib.colors.ListedColormap(
        ((1.0, 1.0, 0.9, 0), (0.975, 0.975, 0.95 * 0.975, 1.0))
    ),
    vmin=0,
    vmax=1,
    alpha=1.0,
    zorder=50,
)


fig.savefig("wind_words.webp")
