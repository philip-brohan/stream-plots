# function to plot the contents of the row 4 and 5 Left panel

from matplotlib.patches import Polygon
from utils import smoothLine, colours, viridis
import numpy as np


def p4L_5L(fig, gspec):
    ax_4L_5L = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_4L_5L.set_facecolor(colours["transparent"])
    ax_4L_5L.spines["right"].set_visible(False)
    ax_4L_5L.spines["top"].set_visible(False)
    # Ground shading with a clipped gradient
    phi = 0.5 * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]], [v @ [0, 0], v @ [0, 1]]])
    a, b = (0, 1)
    X = a + (b - a) / X.max() * X
    im = ax_4L_5L.imshow(
        X,
        interpolation="bicubic",
        clim=(0, 1),
        aspect="auto",
        extent=(100, 0, 0, 1),
        cmap=viridis,
        alpha=0.5,
    )
    im.set_clip_path(
        Polygon([[0, 0], [0, 0.4], [100, 0.6], [100, 0]], transform=ax_4L_5L.transData)
    )

    return ax_4L_5L
