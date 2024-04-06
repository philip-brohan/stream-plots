# function to plot the contents of the rows 2 and 3 and Centre-Left panel

from utils import smoothLine, colours, viridis
import numpy as np


def p2CL_3CL(fig, gspec):
    ax_2CL_3CL = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_2CL_3CL.set_facecolor(colours["transparent"])
    ax_2CL_3CL.spines["right"].set_visible(False)
    ax_2CL_3CL.spines["top"].set_visible(False)
    xy = np.array(
        [
            [5, 0.65],
            [3, 0.58],
            [4, 0.49],
            [5, 0.4],
            [2, 0.05],
            [5, 0.15],
            [15, 0.55],
            [25, 0.51],
            [20, 0.4],
            [12, 0.12],
            [17, 0.1],
            [22, -0.02],
            [28, 0.05],
            [22, 0.14],
            [20, 0.25],
            [27, 0.24],
            [33, 0.13],
            [38, 0.04],
        ]
    )
    colors = viridis(np.random.rand(len(xy)))
    size = 1000
    ax_2CL_3CL.scatter(xy[:, 0], xy[:, 1], c=colors, s=size, alpha=0.5)
    ax_2CL_3CL.scatter(xy[:, 0], xy[:, 1], c="white", s=size / 4, alpha=0.5)

    return ax_2CL_3CL
