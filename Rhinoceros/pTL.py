# function to plot the contents of the Top Left panel

from utils import smoothLine, colours
import numpy as np


def pTL(fig, gspec):
    ax_TL = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_TL.set_facecolor(colours["ax_bg"])
    ax_TL.spines["right"].set_visible(False)
    ax_TL.spines["top"].set_visible(False)
    # Polygon points matched to original
    poly_TL = smoothLine(np.array([[35, 0], [50, 0.3], [100, 0.7]]), k=2)
    # Close the polygon by inserting elements outside of the axes window
    poly_TL = np.append(poly_TL, [[100, 0.0]], axis=0)
    ax_TL.fill_between(
        poly_TL[:, 0],
        poly_TL[:, 1],
        color="none",
        edgecolor=colours["purple"],
        linewidth=5,
        hatch="*",
    )
    return ax_TL
