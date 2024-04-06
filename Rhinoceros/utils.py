# utility functions for the Rhinoceros plot

import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib

viridis = matplotlib.cm.get_cmap("viridis")

colours = {
    "yellow": viridis.colors[255],
    "green": viridis.colors[200],
    "blue": viridis.colors[100],
    "purple": viridis.colors[0],
    "background": (242 / 255, 231 / 255, 218 / 255, 1),
    "transparent": (1, 1, 1, 0.5),
}


# Utility fn to make a smooth line from segments
def smoothLine(pts, n=100, horizontal=True):
    if horizontal:
        spline = make_interp_spline(pts[:, 0], pts[:, 1], k=3)
        x = np.linspace(pts[:, 0].min(), pts[:, 0].max(), n)
        y = spline(x)
    else:
        spline = make_interp_spline(pts[:, 1], pts[:, 0], k=3)
        y = np.linspace(pts[:, 1].min(), pts[:, 1].max(), n)
        x = spline(y)
    return np.stack([x, y], axis=1)
