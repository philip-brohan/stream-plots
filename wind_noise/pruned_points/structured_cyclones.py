#!/usr/bin/env python
# Wind vector plot - for custom wind field.
# Plots anti-aliased vectors rather than advecting points.
# Prunes the vectors before plotting to remove overlap
# Vary the stroke width to simulate brushstrokes and show direction
# Arrange the cyclones in an organised pattern


import os
import sys
import iris
import iris.coords
import iris.coord_systems
import iris.fileformats
import iris.util
import numpy as np
import PIL.Image
from aggdraw import Draw, Pen
from scipy.stats.qmc import PoissonDisk
import pickle
from math import copysign
from Met_palettes import MET_PALETTES

mCols = list(MET_PALETTES["Lakota"]["colors"])


plot_width = 10000
plot_height = 5000
iterations = 10
pen_c = []
for cidx in range(len(mCols)):
    pen_a = []
    for idx in range(iterations):
        pen_a.append(Pen(mCols[cidx], idx * 4 + 1))
    pen_c.append(pen_a)
epsilon = 0.05
poisson_radius = 0.004 / 2
pen = Pen("red", 15)
bgcol = (225, 225, 225)
penb = None # Pen(bgcol,20)
data_resolution = 0.2
prune_distance = 0.8
cyclone_separation = 0.07

# COP colour scheme
COP_white = (1.0, 1.0, 1.0)
COP_blue = (55 / 255, 52 / 255, 139 / 255)
COP_green = (140 / 255, 219 / 255, 114 / 255)


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


# Add alternative cyclone (circular wind field)
def add_cyclone2(u, v, x, y, idx, ci, cs, strength=10, rsq1=20, decay=10):
    lats = u.coord("latitude").points
    lons = v.coord("longitude").points
    lons_g, lats_g = np.meshgrid(lons, lats)
    rsq = (lons_g - x) ** 2 + (lats_g - y) ** 2
    tx = 1 * (lats_g - y) / rsq
    ty = 1 * (lons_g - x) / rsq
    speed = lons_g.copy()
    speed[rsq <= rsq1] = strength * rsq[rsq <= rsq1] / rsq1
    speed[rsq > rsq1] = strength * rsq1 / (rsq1 + rsq[rsq > rsq1] * (decay / 100000))
    spd = np.hypot(speed*tx,speed*ty)
    ci.data = np.where(spd > cs.data,idx,ci.data)
    cs.data = np.where(spd > cs.data,spd,cs.data)
    u.data += speed * tx
    v.data += speed * ty
    return (u, v, ci, cs)


# Use bridson to provide cyclone locations
engine = PoissonDisk(d=2, radius=cyclone_separation)
sample = engine.fill_space()
sample = sample * 360 - 180
sample = sample[(sample[:, 1] > -90) & (sample[:, 1] < 90)]
u10m.data += 5
c_speed = u10m.copy()
c_idx = c_speed.copy()
c_idx.data *= 0

if os.path.isfile("structured_fields.pkl"):
    (u10m, v10m, c_idx, c_speed) = pickle.load(open("structured_fields.pkl", "rb"))
else:
    if os.path.isfile("structured_cyclones.pkl"):
        cyclones = pickle.load(open("structured_cyclones.pkl", "rb"))
    else:
        cyclones = []
        for ci in range(sample.shape[0]):
            cyclone = [
                sample[ci, 0],
                sample[ci, 1],
                np.random.random() * 200 - 100,
                np.random.random() * 100,
                np.random.random() * 10,
            ]
            lat_fraction = (cyclone[0] + 180) / 360
            cyclone[2] = copysign(lat_fraction * 125, cyclone[2])
            cyclones.append(cyclone)
        #pickle.dump(cyclones, open("structured_cyclones.pkl", "wb"))

    for idx in range(len(cyclones)):
        cyclone = cyclones[idx]
        u10m, v10m, c_idx, c_speed = add_cyclone2(
            u10m,
            v10m,
            cyclone[0],
            cyclone[1],
            idx+1,
            c_idx,
            c_speed,
            strength=cyclone[2],
            rsq1=cyclone[3],
            decay=cyclone[4],
        )

    #pickle.dump((u10m, v10m, c_idx, c_speed), open("structured_fields.pkl", "wb"))

# Generate a set of origin points for the wind vectors
opx = []
opy = []
for i in range(-180, 180, 5):
    for j in range(-90, 90, 5):
        opx.append(i)
        opy.append(j)
engine = PoissonDisk(d=2, radius=poisson_radius)
sample = engine.fill_space()
np.random.shuffle(sample)
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


# Prune the wind vectors
def prune(op, prune_radius, coarse_boxes=(20, 10)):
    deleted = set()
    keep = set()
    grid_x = x_to_i(op[:, 0, 0], coarse_boxes[0])
    grid_y = y_to_j(op[:, 1, 0], coarse_boxes[1])
    for row in range(op.shape[0]):
        if row in deleted:
            continue
        src_idx = (grid_x[row], grid_y[row])
        tgt_idx = np.where(
            (grid_x - src_idx[0] < 2)
            & (grid_x - src_idx[0] > -2)
            & (grid_y - src_idx[1] < 2)
            & (grid_y - src_idx[1] > -2)
        )[0]
        # get min distance between any point in row, and all start points
        src_x = op[row, 0, :]
        tgt_x = op[tgt_idx, 0, :]
        dif_x = np.subtract.outer(tgt_x, src_x)
        src_y = op[row, 1, :]
        tgt_y = op[tgt_idx, 1, :]
        dif_y = np.subtract.outer(tgt_y, src_y)
        dif_h = np.amin(np.hypot(dif_x, dif_y), axis=(1, 2))
        # indices of rows where distance is small
        del_r = tgt_idx[np.where(dif_h < prune_radius)[0]]
        # Don't want to match the source row
        del_r = np.delete(del_r, np.where(del_r == row))
        # If overlaps with a line we've already processed, delete this line
        if len(set(del_r) & keep) > 0:
            deleted.add(row)
        else:
            # Keep this line and delete anything it overlaps with
            keep.add(row)
            deleted.update(del_r)
    op = np.delete(op, list(deleted), axis=0)
    return op


line_points = wind_vectors(
    u10m,
    v10m,
    opx,
    opy,
    epsilon=epsilon,
    iterations=iterations,
)

line_points = prune(line_points, prune_distance)


def render_lines(img, op, pen, penb=None):
    draw = Draw(img)

    lp = np.empty(((iterations + 1) * 2))
    for line in range(op.shape[0]):
        lp[0::2] = x_to_i(op[line, 0, :], plot_width)
        lp[1::2] = y_to_j(op[line, 1, :], plot_height)
        col = int(c_idx.data[y_to_j(op[line, 1, 0],dheight),x_to_i(op[line, 0, 0],dwidth)])%len(mCols)
        for segment in range(iterations):
            sidx = segment * 4
            draw.line(lp[sidx : (sidx + 6)], pen_c[col][segment])
    return draw

img = PIL.Image.new(mode="RGB", size=(plot_width, plot_height), color=bgcol)
#img=PIL.Image.fromarray(np.random.randint(0,256,(plot_height,plot_width,3), dtype=np.uint8), mode='RGB')
result = render_lines(img, line_points, pen, penb=penb)
result.flush()

img.save("structured_cyclones.png")
