# function to plot the contents of the row 3 Centre Right panel

from utils import smoothLine, colours, viridis
import numpy as np
import matplotlib
from scipy.stats.qmc import PoissonDisk


def p3CR(fig, gspec):
    ax_3CR = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_3CR.set_facecolor(colours["ax_bg"])
    ax_3CR.spines["right"].set_visible(False)
    ax_3CR.spines["top"].set_visible(False)

    # Shoulder/neck dividing line
    divl = smoothLine(
        np.array([[52, 0], [60, 0.4], [65, 0.8], [67, 1.0]]),
        horizontal=False,
    )
    # Convert to a patch for the shoulder plate
    shoulderP = np.append(divl, [[0, 1], [0, 0]], axis=0)
    shoulderP[:, 0] -= 2  # Make a gap between the plates
    shoulder_patch = matplotlib.patches.Polygon(
        shoulderP,
        facecolor=colours["ax_bg"],
        edgecolor=(0, 0, 0, 0.2),
        linewidth=0,
        zorder=200,
    )
    ax_3CR.add_patch(shoulder_patch)

    # Generate a set of random points for the shoulder plate
    engine = PoissonDisk(d=2, radius=0.05)
    points = engine.fill_space()
    points[:, 0] *= 110
    points[:, 0] -= 5
    points[:, 1] *= 1.1
    points[:, 1] -= 0.05
    z = np.random.rand(points.shape[0])
    tri = matplotlib.tri.Triangulation(points[:, 0], points[:, 1] * 100)
    tripcolor = ax_3CR.tripcolor(
        points[:, 0],
        points[:, 1],
        z,
        triangles=tri.triangles,
        zorder=250,
        cmap=viridis,
    )
    tripcolor.set_clip_path(shoulder_patch)
    # Plot the edges of the triangles over the tripcolor plot
    tri2 = ax_3CR.triplot(
        points[:, 0],
        points[:, 1],
        tri.triangles,
        color=colours["ax_bg"],
        linewidth=4,
        zorder=251,
    )
    for element in tri2:
        element.set_clip_path(shoulder_patch)

    # Make a patch for the neck
    neckP = np.append(divl, [[100, 1], [100, 0]], axis=0)
    neck_patch = matplotlib.patches.Polygon(
        neckP,
        facecolor=colours["ax_bg"],
        edgecolor=(0, 0, 0, 0.2),
        linewidth=0,
        zorder=100,
    )
    ax_3CR.add_patch(neck_patch)
    origin_x = 150
    origin_y = 0.5
    z = np.sqrt((points[:, 0] - origin_x) ** 2 + ((points[:, 1] - origin_y) * 100) ** 2)
    triCF = ax_3CR.tricontourf(
        points[:, 0],
        points[:, 1],
        z,
        triangles=tri.triangles,
        zorder=150,
        cmap=viridis,
    )
    triCF.set_clip_path(neck_patch)
    # Plot the edges of the contour regions over the top
    triL = ax_3CR.tricontour(
        points[:, 0],
        points[:, 1],
        z,
        triangles=tri.triangles,
        zorder=151,
        colors="black",
        linewidth=3,
    )
    triL.set_clip_path(neck_patch)

    return ax_3CR
