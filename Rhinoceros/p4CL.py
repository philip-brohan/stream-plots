# function to plot the contents of the row 4 Centre-Left panel

from utils import smoothLine, colours
import numpy as np


def p4CL(fig, gspec):
    ax_4CL = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_4CL.set_facecolor(colours["transparent"])
    ax_4CL.spines["right"].set_visible(False)
    ax_4CL.spines["top"].set_visible(False)

    return ax_4CL
