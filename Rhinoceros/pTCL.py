# function to plot the contents of the Top Centre-Left panel

from utils import smoothLine, colours
import numpy as np


def pTCL(fig, gspec):
    ax_TCL = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_TCL.set_facecolor(colours["transparent"])
    ax_TCL.spines["right"].set_visible(False)
    ax_TCL.spines["top"].set_visible(False)
    # Line points matched to original
    line_TCL1 = smoothLine(
        np.array(
            [
                [0, 0.72],
                [5, 0.82],
                [10, 0.72],
                [20, 0.68],
                [30, 0.65],
                [40, 0.63],
                [50, 0.6],
                [75, 0.63],
                [100, 0.65],
            ]
        )
    )
    line_TCL2 = smoothLine(
        np.array(
            [
                [0, 0.3],
                [2, 0.4],
                [4, 0.5],
                [5, 0.82],
            ]
        )
    )
    line_TCL2 = np.append([[5.1, 0.0]], line_TCL2, axis=0)

    return ax_TCL
