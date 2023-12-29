#!/usr/bin/env python
# Wind vector plot - for custom wind field.
# Plots anti-aliased vectors rather than advecting points.
# Prunes the vectors before plotting to remove overlap
# Make a random vector field using gstools


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
import gstools as gs

plot_width=10000
plot_height=5000
iterations=10
epsilon=0.05/4
poisson_radius = 0.005
pen = Pen("red",15)
bgcol = (225,225,225)
penb = None #Pen(bgcol,20)
data_resolution=1.0
prune_distance=1.0

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

# import gstools as gs

# the grid
lats = u10m.coord('latitude').points
lons = u10m.coord('longitude').points

# a smooth Gaussian covariance model
model = gs.Gaussian(dim=2, var=1, len_scale=10)
srf = gs.SRF(model, generator="VectorField", seed=19841203)
field = srf((lats, lons), mesh_type="structured")
model = gs.Exponential(dim=2, var=100, len_scale=10)
srf = gs.SRF(model, generator="VectorField", seed=19841203)
field2 = srf((lats, lons), mesh_type="structured")

for idx in range(field.shape[2]):
    weight = 1-idx/field.shape[2]
    u10m.data[:,idx] = field[0,:,idx]*5*weight + field2[0,:,idx]*5*(1-weight)
    v10m.data[:,idx] = field[1,:,idx]*-5*weight+ field2[1,:,idx]*-5*(1-weight)

u10m.data += 20

# Generate a set of origin points for the wind vectors
opx = []
opy = []
for i in range(-180, 180, 5):
    for j in range(-90, 90, 5):
        opx.append(i)
        opy.append(j)
engine=PoissonDisk(d=2,radius=poisson_radius)
sample=engine.fill_space()
sample = sample*360-180
sample = sample[(sample[:,1]>-90) & (sample[:,1]<90)]
opx = sample[:,0]
opy = sample[:,1]

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
def x_to_i(x,width):
    return np.minimum(
        width - 1, np.maximum(0, np.floor((x - xmin) / (xmax - xmin) * (width - 1)))
    ).astype(int)
def y_to_j(y,height):
    return np.minimum(
        height - 1,
        np.maximum(0, np.floor((y - ymin) / (ymax - ymin) * (height - 1))),
    ).astype(int)


# Propagate the origin points with the wind
def wind_vectors(
    uw, vw, opx, opy,iterations=5, epsilon=1
):
    op = np.empty((len(opx),2,iterations+1))
    op[:,0,0] = opx
    op[:,1,0] = opy
    # Repeatedly make a new set of x,y points by moving the previous set with the wind
    for k in range(iterations):
        i = x_to_i(op[:,0,k],dwidth)
        j = y_to_j(op[:,1,k],dheight)
        op[:,0,k+1] = op[:,0,k]+epsilon * uw.data[j, i]
        op[:,0,k+1][op[:,0,k+1] > xmax] = xmax
        op[:,0,k+1][op[:,0,k+1] < xmin] = xmin
        op[:,1,k+1] = op[:,1,k]+epsilon * vw.data[j, i]
        op[:,1,k+1][op[:,1,k+1] > ymax] = ymax
        op[:,1,k+1][op[:,1,k+1] < ymin] = ymin
    return op

# Prune the wind vectors
def prune(op,prune_radius):
    deleted=set()
    keep=set()
    for row in range(op.shape[0]):
        if row in deleted:
            continue
        # get min distance between any point in row, and all start points
        src_x = op[row,0,:]
        tgt_x = op[:,0,:]
        dif_x = np.subtract.outer(tgt_x,src_x)
        src_y = op[row,1,:]
        tgt_y = op[:,1,:]
        dif_y = np.subtract.outer(tgt_y,src_y)
        dif_h = np.amin(np.hypot(dif_x,dif_y),axis=(1,2))
        # indices of rows where distance is small
        del_r = np.where(dif_h<prune_radius)[0]
        # Don't want to match the source row
        del_r = np.delete(del_r,np.where(del_r==row))
        # If overlaps with a line we've already processed, delete this line
        if len(set(del_r) & keep)>0:
            deleted.add(row)
        else:
            # Keep this line and delete anything it overlaps with
            keep.add(row)
            deleted.update(del_r)
    op = np.delete(op,list(deleted),axis=0)
    return(op)


line_points = wind_vectors(
    u10m,
    v10m,
    opx,
    opy,
    epsilon=epsilon,
    iterations=iterations,
)

line_points = prune(line_points,prune_distance)

def render_lines(img,op,pen,penb=None):
    draw = Draw(img)

    lp = np.empty(((iterations+1)*2)) 
    for line in range(op.shape[0]):
        lp[0::2] = x_to_i(op[line,0,:],plot_width)
        lp[1::2] = y_to_j(op[line,1,:],plot_height)
        if penb is not None:
            draw.line(lp,penb)
        draw.line(lp, pen)
    return draw

img = PIL.Image.new(mode='RGB',size=(plot_width,plot_height),color=bgcol)
result = render_lines(img,line_points,pen,penb=penb)
result.flush()

img.save("gst_agg_plot.png")
