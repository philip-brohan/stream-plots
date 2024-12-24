# Functions to check for plot collisions

# Set up a grid covering the plot field, and flag each grid-square where something has been plotted.
# We can use this to check if a new plot element will overlap with an existing one
#  (as long as we have the x,y coordinates of the plot elements in the same units as the grid).

import numpy as np


# Collision cube is a iris cube
# x, y are the coordinates of the plot element
def collision_check(collision_cube, x, y, update=True):
    xc = collision_cube.coords()[1].points
    xmin = np.min(xc)
    xmax = np.max(xc)
    yc = collision_cube.coords()[0].points
    ymin = np.min(yc)
    ymax = np.max(yc)
    i = np.array(
        (((x - xmin) / (xmax - xmin)) * collision_cube.data.shape[1]).astype(int)
    )
    j = np.array(
        (((y - ymin) / (ymax - ymin)) * collision_cube.data.shape[0]).astype(int)
    )
    i[i >= collision_cube.data.shape[1] - 1] = collision_cube.data.shape[1] - 2
    j[j >= collision_cube.data.shape[0] - 1] = collision_cube.data.shape[0] - 2
    i[i < 1] = 1
    j[j < 1] = 1
    if np.sum(collision_cube.data[j, i]) != 0:
        return True
    else:
        if update:
            for k in range(-1, 2):
                for l in range(-1, 2):
                    collision_cube.data[j + k, i + l] = 1
        return False


# Shorten the x and y to remove trailing colliding points
def collision_cut(collision_cube, x, y):
    xc = collision_cube.coords()[1].points
    xmin = np.min(xc)
    xmax = np.max(xc)
    yc = collision_cube.coords()[0].points
    ymin = np.min(yc)
    ymax = np.max(yc)
    i = np.array(
        (((x - xmin) / (xmax - xmin)) * collision_cube.data.shape[1]).astype(int)
    )
    j = np.array(
        (((y - ymin) / (ymax - ymin)) * collision_cube.data.shape[0]).astype(int)
    )
    i[i >= collision_cube.data.shape[1] - 1] = collision_cube.data.shape[1] - 2
    j[j >= collision_cube.data.shape[0] - 1] = collision_cube.data.shape[0] - 2
    i[i < 1] = 1
    j[j < 1] = 1
    if np.sum(collision_cube.data[j, i]) != 0:
        nonzero_indices = np.nonzero(collision_cube.data[j, i])[0]
        x = x[: nonzero_indices[0]]
        y = y[: nonzero_indices[0]]
        return x, y
    else:
        return x, y
