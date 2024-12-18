# Functions for ,anipulating Matplotlib textPaths

import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.transforms import Affine2D
from scipy.interpolate import splprep, splev, interp1d
from copy import deepcopy


# Convert a string to a TextPath
# They don't really have the same units - choose the size appropriately
# or use the transformation factors sx, sy
# sy is -ve by default as I like to have coordinates running bottom to top of the plot
def string_to_path(txt, fsize=4, fprop="Serif", sx=1, sy=-1):
    opath = TextPath(
        (0, 0),  # Arbitrary origin - we're not going to plot it - just get its size
        txt,
        size=fsize,
        prop=fprop,
    )
    otransform = Affine2D().scale(sx=1, sy=-1)
    opath = otransform.transform_path(opath)
    return opath


# Find the length of a curve
def curve_length(x, y):
    dx = np.diff(x)
    dy = np.diff(y)
    distances = np.sqrt(dx**2 + dy**2)
    return np.sum(distances)


# Find the length of a path - assumes the path is straight
def path_length(path):
    Vx = path.vertices[:, 0]
    return np.max(Vx) - np.min(Vx)


# Trim a curve to a given length
def trim_curve(x, y, length):
    dx = np.diff(x)
    dy = np.diff(y)
    distances = np.sqrt(dx**2 + dy**2)
    distances = np.cumsum(distances)
    idx = np.argmax(distances > length)
    return x[:idx], y[:idx]


# Map a textPath onto a curve [x,y]
# path is the textPath to be mapped
# x,y are the curve to map onto - numpy arrays
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


# Render a single text string along a curve
# ax is the matplotlib axis to render to
# txt is the text string to render
# x,y are the curve to render along - numpy arrays, in ax data units
# colour is the colour of the text
# collision_cube is a cube of points to avoid rendering collisions
# Returns a TextPath object
def string_to_patch(
    ax, txt, x, y, colour="black", fsize=4, fprop="Serif", collision_cube=None
):
    opath = TextPath(
        (x[0], y[0]),
        txt,
        size=fsize,
        prop=fprop,
    )
    otransform = Affine2D().scale(sx=1, sy=-1)  # y runs bottom to top
    opath = otransform.transform_path(opath)
    # Map the textPath onto the curve
    npath = map_path(opath, x, y)
    return npath
