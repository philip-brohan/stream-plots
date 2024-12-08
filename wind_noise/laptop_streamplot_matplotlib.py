#!/usr/bin/env python
# Wind vector plot - for custom wind field.
# Plots anti-aliased vectors rather than advecting points.
# Matplotlib version

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
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

pscale = 10
pwidth = 5
plot_width = 1000 * pscale
plot_height = 500 * pscale
iterations = 50
epsilon = 0.05 / 2
poisson_radius = 0.005 * 1
pen = []
scheme = MET_PALETTES["Hokusai2"]
bgcol = (225, 225, 225)
data_resolution = 0.2


def plot_cube(resolution, xmin=-180, xmax=180, ymin=-90, ymax=90):
    cs = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
    lat_values = np.flip(np.arange(ymin, ymax + resolution, resolution))
    latitude = iris.coords.DimCoord(
        lat_values, standard_name="latitude", units="degrees_north", coord_system=cs
    )
    lon_values = np.arange(xmin, xmax + resolution, resolution)
    longitude = iris.coords.DimCoord(
        lon_values, standard_name="longitude", units="degrees_east", coord_system=cs
    )
    dummy_data = np.zeros((len(lat_values), len(lon_values)))
    plot_cube = iris.cube.Cube(
        dummy_data, dim_coords_and_dims=[(latitude, 0), (longitude, 1)]
    )
    return plot_cube


u10m = plot_cube(data_resolution)
v10m = u10m.copy()


# Add a cyclone (circular wind field)
def add_cyclone(u, v, x, y, strength=10, decay=0.1):
    lats = u.coord("latitude").points
    lons = v.coord("longitude").points
    lons_g, lats_g = np.meshgrid(lons, lats)
    rsq = (lons_g - x) ** 2 + (lats_g - y) ** 2
    rsq[rsq < 1] = 1
    tx = 1 * (lats_g - y) / rsq
    ty = 1 * (lons_g - x) / rsq
    speed = strength / (1.0 + rsq * decay)
    u.data += speed * tx
    v.data += speed * ty
    return (u, v)


for cyclone in [[180, 100, 20, 0.0001], [90, 45, 100, 0.0001], [0, 0, 100, 0.0001]]:
    u10m, v10m = add_cyclone(
        u10m, v10m, cyclone[0], cyclone[1], strength=cyclone[2], decay=cyclone[3]
    )
u10m.data += 2  # 2
speed = np.sqrt(u10m.data**2 + v10m.data**2)
min_speed = 0.75
max_speed = 3
v10m.data[speed < min_speed] *= min_speed / v10m.data[speed < min_speed]
u10m.data[speed < min_speed] *= min_speed / u10m.data[speed < min_speed]
v10m.data[speed > max_speed] *= max_speed / speed[speed > max_speed]
u10m.data[speed > max_speed] *= max_speed / speed[speed > max_speed]

# Generate a set of origin points for the wind vectors
opx = []
opy = []
for i in range(-180, 180, 5):
    for j in range(-90, 90, 5):
        opx.append(i)
        opy.append(j)
engine = PoissonDisk(d=2, radius=poisson_radius)
sample = engine.fill_space()
sample = sample * 360 - 180
sample = sample[(sample[:, 1] > -90) & (sample[:, 1] < 90)]
opx = sample[:, 0]
opy = sample[:, 1]

# Each point in this field has an index location (i,j)
#  and a real (x,y) position
xc = u10m.coords()[1].points
xmin = np.min(xc)
xmax = np.max(xc)
dwidth = len(xc)
yc = u10m.coords()[0].points
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
        op[:, 0, k + 1] = op[:, 0, k] + epsilon * uw.data[j, i]
        op[:, 0, k + 1][op[:, 0, k + 1] > xmax] = xmax
        op[:, 0, k + 1][op[:, 0, k + 1] < xmin] = xmin
        op[:, 1, k + 1] = op[:, 1, k] + epsilon * vw.data[j, i]
        op[:, 1, k + 1][op[:, 1, k + 1] > ymax] = ymax
        op[:, 1, k + 1][op[:, 1, k + 1] < ymin] = ymin
    return op


line_points = wind_vectors(
    u10m,
    v10m,
    opx,
    opy,
    epsilon=epsilon,
    iterations=iterations,
)
# print(line_points[100,:,:])
# sys.exit(0)

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

count = 0
for line in range(line_points.shape[0]):
    ax.add_line(
        Line2D(
            line_points[line, 0, :],
            line_points[line, 1, :],
            color=scheme["colors"][count % len(scheme)],
            linewidth=pwidth,
        )
    )
    count += 1


fig.savefig("laptop_streamplot_matplotlib.webp")
