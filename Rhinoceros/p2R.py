# function to plot the contents of the row 2  Right panel

from utils import smoothLine, colours, viridis
import numpy as np


def p2R(fig, gspec):
    ax_2R = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_2R.set_facecolor(colours["transparent"])
    ax_2R.spines["right"].set_visible(False)
    ax_2R.spines["top"].set_visible(False)

    return ax_2R
