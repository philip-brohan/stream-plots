#!/usr/bin/env python
# Background plot of the cyclone arrangement

import os
import sys
import iris
import iris.coords
import iris.coord_systems
import iris.fileformats
import iris.util
import numpy as np
import PIL.Image
from scipy.stats.qmc import PoissonDisk
from math import copysign
from Met_palettes import MET_PALETTES

mCols = list(MET_PALETTES["Hokusai2"]["colors"])

plot_width = 1000
plot_height = 500
plot_resolution = 360/plot_width
cyclone_separation = 0.07

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


u10m = plot_cube(plot_resolution)
v10m = u10m.copy()
(plot_height,plot_width)=u10m.data.shape 


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
    ospd = np.hypot(u.data,v.data)
    spd = np.hypot(speed*tx,speed*ty)
    rnd = np.random.default_rng().random(size=ci.data.shape)
    threshold = 1.0-0.3*strength/100
    ci.data = np.where((abs(spd)>5) & (rnd>threshold),idx,ci.data)
    ci.data = np.where((rsq < rsq1) & (rnd>threshold),idx,ci.data)
    u.data += speed*tx
    v.data += speed*ty
    return (u, v, ci, cs)


# Use bridson to provide cyclone locations
engine = PoissonDisk(d=2, radius=cyclone_separation)
sample = engine.fill_space()
sample = sample * 360 - 180
sample = sample[(sample[:, 1] > -90) & (sample[:, 1] < 90)]
u10m.data += 5
c_speed = u10m.copy()
c_idx = c_speed.copy()
c_idx.data = np.random.randint(0,2,c_idx.data.shape)

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

for idx in range(len(cyclones)):
    cyclone = cyclones[idx]
    u10m, v10m, c_idx, c_speed = add_cyclone2(
        u10m,
        v10m,
        cyclone[0],
        cyclone[1],
        len(mCols)-1,
        c_idx,
        c_speed,
        strength=cyclone[2],
        rsq1=cyclone[3],
        decay=cyclone[4],
    )

pix_cidx = c_idx.data.astype(int)
pix_cidx = np.where(pix_cidx>0,pix_cidx%(len(mCols)-2)+2,0)
pix_cols = np.random.randint(0,256,(plot_height,plot_width,3), dtype=np.uint8)
for idx in range(len(mCols)):
    col = tuple(int(mCols[idx][i:i+2], 16) for i in (1, 3, 5))
    for channel in (0,1,2):
        pix_cols[:,:,channel]=np.where(pix_cidx==idx,col[channel],pix_cols[:,:,channel])

img=PIL.Image.fromarray(pix_cols,mode='RGB')
img = img.resize((10000,5000),resample=PIL.Image.BICUBIC)

img.save("coloured_cyclones.png")
