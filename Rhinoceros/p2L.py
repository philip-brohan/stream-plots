# function to plot the contents of the row 2 Left panel

from utils import smoothLine, colours, viridis
import numpy as np


def p2L(fig, gspec):
    ax_2L = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_2L.set_facecolor(colours["transparent"])
    ax_2L.spines["right"].set_visible(False)
    ax_2L.spines["top"].set_visible(False)
    # Polygon points matched to original
    poly_2L = smoothLine(
        np.array([[78, -0.1], [75, 0], [73, 0.25], [78, 0.65], [90, 1], [100, 1.1]]),
        horizontal=False,
    )
    # Draw the line to be a shadow effect
    ax_2L.plot(
        poly_2L[:, 0],
        poly_2L[:, 1],
        color=(0, 0, 0, 0.2),
        linewidth=10,
        marker="none",
        zorder=200,
    )
    # Close the polygon by inserting elements outside of the axes window
    poly_2L = np.append(poly_2L, [[110, 1.1], [110, -0.1]], axis=0)
    ax_2L.fill_between(
        poly_2L[:, 0],
        poly_2L[:, 1],
        color=(1, 0, 0, 0.25),  # bgcolor,
        edgecolor="none",
        zorder=300,
    )
    xy = np.array(
        [
            [80, 0.25],
            [83, 0.58],
            [86, 0.35],
            [89, 0.4],
            [92, 0.10],
            [95, 0.85],
            [98, 0.50],
            [95, 0.28],
            [90, 0.70],
        ]
    )
    colors = viridis(np.random.rand(len(xy)))
    size = 1000
    ax_2L.scatter(xy[:, 0], xy[:, 1], c=colors, s=size, marker="*", alpha=0.5)

    return ax_2L
