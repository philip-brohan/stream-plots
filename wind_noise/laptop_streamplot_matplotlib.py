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
from matplotlib.lines import Line2D
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D
from scipy.interpolate import make_interp_spline
from scipy.interpolate import splprep, splev, interp1d
from copy import deepcopy
import random

from scipy.stats import gamma

# Load the shipping forecast
with open("./forecast.txt", "r") as file:
    # Read all lines into a list of strings
    lines = file.readlines()

# Remove blank lines from the list
lines = [line.strip() for line in lines if line.strip()]
olines = deepcopy(lines)

pscale = 10
pwidth = 5
plot_width = 1000 * pscale
plot_height = 500 * pscale
iterations = 50
epsilon = 0.05 / 2
poisson_radius = 0.005 * 1
pen = []
scheme = MET_PALETTES["Hokusai2"]
txt_scheme = MET_PALETTES["Signac"]
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

# Use a grid to keep track of collisions
collision_cube = plot_cube(1.0)
collision_cube.data = np.zeros(collision_cube.data.shape)


# Check a line for collision with previous lines
def collision_check(collision_cube, x, y):
    i = np.array((((x + 180) / 360) * collision_cube.data.shape[1]).astype(int))
    j = np.array((((y + 90) / 180) * collision_cube.data.shape[0]).astype(int))
    i[i >= collision_cube.data.shape[1] - 1] = collision_cube.data.shape[1] - 2
    j[j >= collision_cube.data.shape[0] - 1] = collision_cube.data.shape[0] - 2
    i[i < 1] = 1
    j[j < 1] = 1
    if np.sum(collision_cube.data[j, i]) != 0:
        return True
    else:
        for k in range(-1, 2):
            for l in range(-1, 2):
                collision_cube.data[j + k, i + l] = 1
        return False


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
    # Trim the curve to the length of the path
    distances = distances[distances < (np.max(Vx) - np.min(Vx))]
    x = x[: len(distances)]
    y = y[: len(distances)]
    distancesL = distancesL[: len(distances)]
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
    dVxspeed = dVxspeed / np.mean(dVxspeed)
    # Generate the mapped-path vertices
    tan_g = dy / dx
    dscale = 1  # / dVxspeed
    ndVx = -dVy * dscale * tan_g / np.sqrt(1 + tan_g**2)
    ndVy = dVy * dscale / np.sqrt(1 + tan_g**2)
    nVx = nVx + ndVx
    nVy = nVy + ndVy
    # Make the new path with these vertices
    new_path = deepcopy(path)
    new_path.vertices[:, 0] = nVx
    new_path.vertices[:, 1] = nVy
    return new_path


# Add a cyclone (circular wind field)
def add_cyclone(u, v, x, y, strength=10, decay=0.1, shape=1, scale=1):
    lats = u.coord("latitude").points
    lons = v.coord("longitude").points
    lons_g, lats_g = np.meshgrid(lons, lats)
    rsq = (lons_g - x) ** 2 + (lats_g - y) ** 2
    tx = 1 * (lats_g - y) / np.sqrt(rsq)
    ty = 1 * (lons_g - x) / np.sqrt(rsq)
    speed = strength * gamma.pdf(np.sqrt(rsq) / decay, a=shape, loc=0, scale=scale)
    u.data += speed * tx
    v.data += speed * ty
    return (u, v)


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
u10m.data += 2  # 2


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

# Generate a set of origin points for the text strings
engine = PoissonDisk(d=2, radius=poisson_radius * 2)
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
    epsilon=epsilon * 4,
    iterations=iterations * 5,
)

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
ax.set_xlim(-170, 170)
ax.set_ylim(85, -85)
ax.set_aspect("auto")

count = 0
for line in range(line_points.shape[0]):
    ax.add_line(
        Line2D(
            line_points[line, 0, :],
            line_points[line, 1, :],
            color=scheme["colors"][count % len(scheme["colors"])],
            linewidth=pwidth,
            solid_capstyle="round",
            zorder=10,
        )
    )
    count += 1

for txt in range(text_points.shape[0]):
    random_line = None
    try:
        random_line = random.choice(lines)
        opath = TextPath(
            (text_points[txt, 0, 0], text_points[txt, 1, 0]),
            random_line,
            size=4,
            prop="Serif",
        )
        otransform = Affine2D().scale(sx=1, sy=-1)
        opath = otransform.transform_path(opath)
        opatch = PathPatch(
            opath, facecolor="red", edgecolor="white", linewidth=0, zorder=20
        )
        # ax.add_artist(opatch)

        npath = map_path(opath, text_points[txt, 0, :], text_points[txt, 1, :])
        npatch = PathPatch(
            npath,
            facecolor=txt_scheme["colors"][count % len(txt_scheme["colors"])],
            edgecolor="white",
            linewidth=0.5,
            zorder=30,
        )
        if not collision_check(
            collision_cube, text_points[txt, 0, :], text_points[txt, 1, :]
        ):
            ax.add_artist(npatch)
            count += 1
    except Exception as e:
        print(e)
    if random_line is not None:
        lines.remove(random_line)
        if len(lines) == 0:
            lines = deepcopy(olines)

# break


fig.savefig("laptop_streamplot_matplotlib.webp")
