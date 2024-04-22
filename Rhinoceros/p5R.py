# function to plot the contents of the row 5 Right panel

from utils import smoothLine, colours, viridis
import numpy as np


def p5R(fig, gspec):
    ax_5R = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_5R.set_facecolor(colours["ax_bg"])
    ax_5R.spines["right"].set_visible(False)
    ax_5R.spines["top"].set_visible(False)

    # Add a bar chart
    ax_5R.bar(
        [10, 30, 50, 70, 90],
        [0.9, 0.8, 0.75, 0.7, 0.75],
        width=18,
        color="none",
        edgecolor="black",
        hatch="x",
    )

    return ax_5R
