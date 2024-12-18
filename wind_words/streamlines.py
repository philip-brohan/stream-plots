# Functions to make streamlines from wind fields

# Made by forward propagating a set of start points

import numpy as np


# Each point in this field has an index location (i,j)
#  and a real (x,y) position
# Convert between index and real positions
def x_to_i(x, xmin, xmax, width):
    return np.minimum(
        width - 1, np.maximum(0, np.floor((x - xmin) / (xmax - xmin) * (width - 1)))
    ).astype(int)


def y_to_j(y, ymin, ymax, height):
    return np.minimum(
        height - 1,
        np.maximum(0, np.floor((y - ymin) / (ymax - ymin) * (height - 1))),
    ).astype(int)


# Propagate the origin points with the wind
# uw, vw are the wind fields - iris cubes
# opx, opy are the streamline origin points - numpy arrays
def wind_vectors(uw, vw, opx, opy, iterations=5, epsilon=1):
    op = np.empty((len(opx), 2, iterations + 1))
    op[:, 0, 0] = opx
    op[:, 1, 0] = opy
    xc = uw.coords()[1].points
    xmin = np.min(xc)
    xmax = np.max(xc)
    dwidth = len(xc)
    yc = uw.coords()[0].points
    ymin = np.min(yc)
    ymax = np.max(yc)
    dheight = len(yc)
    # Repeatedly make a new set of x,y points by moving the previous set with the wind
    for k in range(iterations):
        i = x_to_i(op[:, 0, k], xmin, xmax, dwidth)
        j = y_to_j(op[:, 1, k], ymin, ymax, dheight)
        op[:, 0, k + 1] = op[:, 0, k] + epsilon * uw.data[j, i]
        op[:, 0, k + 1][op[:, 0, k + 1] > xmax] = xmax
        op[:, 0, k + 1][op[:, 0, k + 1] < xmin] = xmin
        op[:, 1, k + 1] = op[:, 1, k] + epsilon * vw.data[j, i]
        op[:, 1, k + 1][op[:, 1, k + 1] > ymax] = ymax
        op[:, 1, k + 1][op[:, 1, k + 1] < ymin] = ymin
    return op
