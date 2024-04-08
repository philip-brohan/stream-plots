# function to plot the contents of the Top Right and Centre-Right panel

from utils import smoothLine, colours
import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D


def pTCR_TR(fig, gspec):
    ax_TCR_TR = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_TCR_TR.set_facecolor(colours["transparent"])
    ax_TCR_TR.spines["right"].set_visible(False)
    ax_TCR_TR.spines["top"].set_visible(False)

    # Straight line segments - heavy lines for outline
    x = np.array([[0, 3]]).T
    y = np.array([[0.66, 0.63]]).T

    x = np.concatenate([x, np.array([[1, 2], [3, 11], [11, 13]]).T], axis=1)
    y = np.concatenate([y, np.array([[0, 0.5], [0.55, 0.35], [0.32, 0]]).T], axis=1)

    x = np.concatenate([x, np.array([[5, 4], [5, 21], [22, 29]]).T], axis=1)
    y = np.concatenate([y, np.array([[0.54, 0.7], [0.7, 0.45], [0.45, 0.3]]).T], axis=1)

    x = np.concatenate([x, np.array([[30, 39], [39, 31]]).T], axis=1)
    y = np.concatenate([y, np.array([[0.3, 0.45], [0.45, 0.15]]).T], axis=1)

    x = np.concatenate([x, np.array([[31, 34], [34.5, 35.5]]).T], axis=1)
    y = np.concatenate([y, np.array([[0.0, 0.16], [0.17, 0.14]]).T], axis=1)

    x = np.concatenate([x, np.array([[33, 36], [36.5, 39.5]]).T], axis=1)
    y = np.concatenate([y, np.array([[0.0, 0.14], [0.14, 0.05]]).T], axis=1)

    x = np.concatenate([x, np.array([[38, 41], [41.5, 43.5], [44, 46]]).T], axis=1)
    y = np.concatenate(
        [y, np.array([[0.0, 0.07], [0.07, 0.07], [0.07, 0.0]]).T], axis=1
    )

    ax_TCR_TR.plot(x, y, color=colours["green"], linewidth=5)

    # - narrow lines as highlights
    x = np.array([[2, 5], [3, 10], [7, 10]]).T
    y = np.array([[0.02, 0.45], [0.02, 0.32], [0.06, 0.06]]).T

    x = np.concatenate([x, np.array([[6, 8], [9, 11]]).T], axis=1)
    y = np.concatenate([y, np.array([[0.65, 0.5], [0.6, 0.5]]).T], axis=1)

    ax_TCR_TR.plot(x, y, color=colours["green"], linewidth=2)

    # Add the title on a curved path
    path = TextPath((40, 14), "RHINOCEROS", size=8, prop="Arial")
    transform = Affine2D().scale(sx=1, sy=0.0356)
    path = transform.transform_path(path)
    path.vertices.setflags(write=1)
    Vx, Vy = path.vertices[:, 0], path.vertices[:, 1]
    nVx = 2 * np.pi * (Vx - Vx.min()) / (Vx.max() - Vx.min())
    Vy += 0.1 * np.sin(nVx)
    patch = PathPatch(
        path, facecolor=colours["blue"], edgecolor=colours["green"], linewidth=3
    )
    ax_TCR_TR.add_artist(patch)

    # Add date
    path = TextPath((75, 20), "2024", size=6, prop="Arial")
    transform = Affine2D().scale(sx=1, sy=0.0356)
    path = transform.transform_path(path)
    patch = PathPatch(
        path, facecolor=colours["green"], edgecolor=colours["blue"], linewidth=3
    )
    ax_TCR_TR.add_artist(patch)

    # Add Logotype
    path = TextPath((50, 9), "P", size=8, prop="Arial")
    transform = Affine2D().scale(sx=1, sy=0.0356)
    path = transform.transform_path(path)
    patch = PathPatch(
        path, facecolor=colours["blue"], edgecolor=colours["blue"], linewidth=0
    )
    ax_TCR_TR.add_artist(patch)
    path = TextPath((52, 9), "B", size=4, prop="Arial")
    transform = Affine2D().scale(sx=1, sy=0.0356)
    path = transform.transform_path(path)
    patch = PathPatch(path, facecolor=colours["green"], linewidth=0)
    ax_TCR_TR.add_artist(patch)

    return ax_TCR_TR
