# function to plot the contents of the Top Right and Centre-Right panel

from utils import smoothLine, colours
import numpy as np


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

    return ax_TCR_TR
