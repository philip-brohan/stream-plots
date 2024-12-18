# Function to define a cyclone in terms of size, strength and shape

import numpy as np
from scipy.stats import gamma


# Add a cyclone (circular wind field) to fields of u and v wind
# u, v are iris cubes of wind fields - on the same grid
# x, y are the centre of the cyclone, in the coordinates used by u and v
# strength is a multiplier for the cyclone wind speeds
# decay controls the overall size - bigger decay gives smaller cyclones
# Shape and scale are standard gamma distribution parameters
def add_cyclone(u, v, x, y, strength=10, decay=0.1, shape=2, scale=1):
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
