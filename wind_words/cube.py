#!/usr/bin/env python

# Cube utility functions

import iris
import iris.coords
import iris.coord_systems
import iris.fileformats
import iris.util
import numpy as np


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
