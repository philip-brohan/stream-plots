# utility functions for the Rhinoceros plot

import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib

viridis = matplotlib.colormaps["viridis"]

colours = {
    "yellow": viridis.colors[255],
    "green": viridis.colors[200],
    "blue": viridis.colors[100],
    "purple": viridis.colors[0],
    "background": (242 / 255, 231 / 255, 218 / 255, 1),
    "transparent": (1, 1, 1, 0.5),
    "ax_bg": (0.975, 0.953, 0.927, 1),  # background+transparent
}


# Utility fn to make a smooth line from segments
def smoothLine(pts, n=100, horizontal=True, k=3):
    if horizontal:
        try:
            spline = make_interp_spline(pts[:, 0], pts[:, 1], k=k)
            x = np.linspace(pts[:, 0].min(), pts[:, 0].max(), n)
            y = spline(x)
        except ValueError:  # If values are decreasing, flip
            spline = make_interp_spline(pts[::-1, 0], pts[::-1, 1], k=k)
            x = np.linspace(pts[:, 0].max(), pts[:, 0].min(), n)
            y = spline(x)
    else:
        try:
            spline = make_interp_spline(pts[:, 1], pts[:, 0], k=k)
            y = np.linspace(pts[:, 1].min(), pts[:, 1].max(), n)
            x = spline(y)
        except ValueError:  # If values are decreasing, flip
            spline = make_interp_spline(pts[::-1, 1], pts[::-1, 0], k=k)
            y = np.linspace(pts[:, 1].max(), pts[:, 1].min(), n)
            x = spline(y)
    return np.stack([x, y], axis=1)
