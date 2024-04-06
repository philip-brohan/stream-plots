# function to plot the contents of the row 5 Centre-Left panel

from utils import smoothLine, colours
import numpy as np


def p5CL(fig, gspec):
    ax_5CL = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_5CL.set_facecolor(colours["transparent"])
    ax_5CL.spines["right"].set_visible(False)
    ax_5CL.spines["top"].set_visible(False)

    # Use a grid to imitate the shading shadow
    ax_5CL.set_yticks(np.linspace(0.2, 0.9, 25), minor=True)
    ax_5CL.grid(
        visible=True,
        which="minor",
        axis="y",
        color="black",
        linestyle="-",
        linewidth=0.5,
    )

    return ax_5CL
