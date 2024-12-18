# Functions to check for plot collisions

# Set up a grid covering the plot field, and flag each grid-square where something has been plotted.
# We can use this to check if a new plot element will overlap with an existing one
#  (as long as we have the x,y coordinates of the plot elements in the same units as the grid).

import numpy as np


# Collision cube is a iris cube
# x, y are the coordinates of the plot element
def collision_check(collision_cube, x, y, update=True):
    i = np.array((((x + 180) / 360) * collision_cube.data.shape[1]).astype(int))
    j = np.array((((y + 90) / 180) * collision_cube.data.shape[0]).astype(int))
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
