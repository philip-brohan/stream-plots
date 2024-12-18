#!/usr/bin/env python

# Plot a wind field using text strings from the shipping forecast

import os
import sys
import iris
import iris.coords
import iris.coord_systems
import iris.fileformats
import iris.util
import numpy as np
from scipy.stats.qmc import PoissonDisk
from Met_palettes import MET_PALETTES
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from copy import deepcopy

import random

from cube import plot_cube
from cyclone import add_cyclone
from streamlines import wind_vectors
from textPath import map_path, string_to_path, curve_length, path_length, trim_curve
from collisions import collision_check

# Parameters
plot_width = 3200
plot_height = 2100

iterations = 250  # How far the streamlines propagate (max)
epsilon = 0.2

poisson_radius = 0.01  # Figure fraction - separation of streamline start points

scheme = MET_PALETTES["Hokusai2"]
bgcol = (225 / 255, 225 / 255, 225 / 255, 1.0)

data_resolution = 0.2  # degrees (units of u wind)
collision_resolution = 0.5  # same

font_size = 3  # Scaling for the TextPath - 4 is about right to match the degrees
fprop = "Serif"  # font choice


# Load the shipping forecast
with open("./forecast.txt", "r") as file:
    # Read all lines into a list of strings
    lines = file.readlines()

# Remove blank lines from the list
lines = [line.strip() for line in lines if line.strip()]

# Make a TextPath for each line (to get the size)
linePaths = {}
for line in lines:
    linePaths[line] = string_to_path(line, fsize=font_size, fprop=fprop)
olinePaths = deepcopy(linePaths)


# Find lines shorter than some given curve
def line_shorter_than(linePaths, x, y):
    max_length = curve_length(x, y)
    short_lines = []
    for line in linePaths:
        if path_length(linePaths[line]) < max_length:
            short_lines.append(line)
    return short_lines


# Set up the wind field
u10m = plot_cube(data_resolution)
v10m = u10m.copy()
u10m.data += 2  # 2

# Use a grid to keep track of collisions
collision_cube = plot_cube(collision_resolution)
collision_cube.data = np.zeros(collision_cube.data.shape)


# Add a bunch of cyclones to the wind field
for ci in range(75):
    lon = np.random.random() * 360 - 180
    cyclone = [
        lon,
        np.random.random() * 180 - 90,
        (np.random.random() * 20 - 10) * (lon + 180) / 360,
        10,
        2,
        1,
    ]
    u10m, v10m = add_cyclone(
        u10m,
        v10m,
        cyclone[0],
        cyclone[1],
        strength=cyclone[2],
        decay=cyclone[3],
        shape=cyclone[4],
        scale=cyclone[5],
    )


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
ax.set_xlim(-170, 170)
ax.set_ylim(85, -85)
ax.set_aspect("auto")

# Generate a set of origin points for the text strings
engine = PoissonDisk(d=2, radius=poisson_radius)
sample = engine.fill_space()
sample = sample * 360 - 180
sample = sample[(sample[:, 1] > -90) & (sample[:, 1] < 90)]
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

# Add the streamlines in random order
line_sequence = random.sample(list(range(text_points.shape[0])), text_points.shape[0])

count = 0
for streamline in line_sequence:
    for trial in range(5):  # Try a few times to get a text string that fits the space
        x = text_points[streamline, 0, :]
        y = text_points[streamline, 1, :]
        short_lines = line_shorter_than(linePaths, x, y)
        if len(short_lines) == 0:
            break
        random_line = random.choice(short_lines)
        x, y = trim_curve(x, y, path_length(linePaths[random_line]))

        npath = map_path(linePaths[random_line], x, y)
        npatch = PathPatch(
            npath,
            # facecolor=scheme["colors"][count % len(scheme["colors"])],
            facecolor="black",
            edgecolor="white",
            linewidth=0.5,
            zorder=30,
        )
        if not collision_check(
            collision_cube, npath.vertices[:, 0], npath.vertices[:, 1]
        ):
            ax.add_artist(npatch)
            count += 1
            # del linePaths[random_line]
            if len(lines) == 0:
                linePaths = deepcopy(olinePaths)
            break


fig.savefig("wind_words.webp")
