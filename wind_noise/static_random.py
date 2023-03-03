#!/usr/bin/env python

# Wind vector plot - for fixed time
# Use random speckle field

import os
import sys

import iris
import iris.coords
import iris.util
import numpy as np

import PIL.Image

z_resolution = 0.5
i_resolution = 0.1

r_file_name = "%s/ERA5/hourly/reanalysis/2018/03/12/15/10m_wind.nc" % os.getenv(
    "SCRATCH"
)
u10m = iris.util.squeeze(iris.load_cube(r_file_name, iris.Constraint(name="u10")))
v10m = iris.util.squeeze(iris.load_cube(r_file_name, iris.Constraint(name="v10")))
coord_s = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
u10m.coord("latitude").coord_system = coord_s
u10m.coord("longitude").coord_system = coord_s
v10m.coord("latitude").coord_system = coord_s
v10m.coord("longitude").coord_system = coord_s


def plot_cube(resolution, xmin=-180, xmax=180, ymin=-90, ymax=90):
    cs = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
    lat_values = np.arange(ymin, ymax + resolution, resolution)
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


# Make the wind noise base field
z = plot_cube(z_resolution)
(width, height) = z.data.shape
z.data=np.sqrt(np.random.rand(width,height))*2-1


def wind_field(
    uw, vw, z, sequence=None, iterations=50, mfraction=0.5, epsilon=0.01, sscale=1
):
    offset = z.copy()
    offset.data *= 0
    #offset.data += 0.5
    ss=uw.copy()
    ss.data=np.sqrt(uw.data**2+vw.data**2)
    z = z.regrid(uw, iris.analysis.Nearest())
    z.data *= ss.data/sscale
    offset = offset.regrid(uw, iris.analysis.Nearest())
    (width, height) = z.data.shape
    # Each point in this field has an index location (i,j)
    #  and a real (x,y) position
    xmin = np.min(uw.coords()[0].points)
    xmax = np.max(uw.coords()[0].points)
    ymin = np.min(uw.coords()[1].points)
    ymax = np.max(uw.coords()[1].points)
    # Convert between index and real positions
    def i_to_x(i):
        return xmin + (i / width) * (xmax - xmin)

    def j_to_y(j):
        return ymin + (j / height) * (ymax - ymin)

    def x_to_i(x):
        return np.minimum(
            width - 1, np.maximum(0, np.floor((x - xmin) / (xmax - xmin) * (width - 1)))
        ).astype(int)

    def y_to_j(y):
        return np.minimum(
            height - 1,
            np.maximum(0, np.floor((y - ymin) / (ymax - ymin) * (height - 1))),
        ).astype(int)

    i, j = np.mgrid[0:width, 0:height]
    x = i_to_x(i)
    y = j_to_y(j)
    # Result is a distorted version of the random field
    result = z.copy()
    # Repeatedly, move the x,y points according to the vector field
    #  and update result with the random field at their locations
    endpoints=iterations+1 
    startpoints=-1       
    for k in range(iterations):
        x += epsilon*vw.data[i,j]
        x[x>xmax]=xmax
        x[x<xmin]=xmin
        y += epsilon*uw.data[i,j]
        y[y>ymax]=y[y>ymax]-ymax+ymin
        y[y<ymin]=y[y<ymin]-ymin+ymax
        i=x_to_i(x)
        j=y_to_j(y)
        update=z.data*ss.data/sscale
        update[(endpoints>startpoints) & ((k>endpoints) | (k<startpoints))]=0
        update[(startpoints>endpoints) & ((k>endpoints) & (k<startpoints))]=0
        #result.data[i,j] += update
        result.data[i,j] = update
    result.data /= np.max((np.max(result.data),np.min(result.data)*-1))
    return result



wind_pc = plot_cube(i_resolution)
wind_noise_field = wind_field(
    u10m,
    v10m,
    z,
    epsilon=0.1,
    iterations=50,
    mfraction=0.75,
    sscale=1,
)

# Convert the wind_noise_field array to an image

r_ch = np.int8((wind_noise_field.data.copy())*255)
g_ch = np.int8((wind_noise_field.data.copy())*255)
b_ch = np.int8((wind_noise_field.data.copy())*255)

rgb_ch = np.stack((r_ch,g_ch,b_ch),axis=2)

img = PIL.Image.fromarray(rgb_ch,mode='RGB')

img.save("static_random.png")
