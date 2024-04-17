# function to plot the contents of the row 4 Centre-Left panel

from utils import smoothLine, colours, viridis
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
    ax_4CL.set_facecolor(colours["ax_bg"])
    ax_4CL.spines["right"].set_visible(False)
    ax_4CL.spines["top"].set_visible(False)

    # Belly curve
    line_B = smoothLine(
        np.array(
            [
                [0, 1.0],
                [20, 0.8],
                [40, 0.7],
                [60, 0.65],
                [80, 0.7],
                [100, 0.75],
            ]
        ),
        n=20,
    )
    markerline, stemlines, baseline = ax_4CL.stem(
        line_B[:, 0],
        line_B[:, 1],
        bottom=1,
        linefmt="-",
        markerfmt="o",
        basefmt=" ",
    )
    stemlines.set_linewidth(5)
    stemlines.set_color(viridis(0))
    markerline.set_markersize(20)
    markerline.set_color(viridis(0))

    # Same for the ground line
    line_G = smoothLine(
        np.array(
            [
                [10, 0.1],
                [20, 0.11],
                [40, 0.16],
                [60, 0.13],
                [80, 0.12],
                [100, 0.15],
            ]
        ),
        n=30,
    )
    markerline, stemlines, baseline = ax_4CL.stem(
        line_G[:, 0],
        line_G[:, 1],
        bottom=0,
        linefmt="-",
        markerfmt="o",
        basefmt=" ",
    )
    stemlines.set_linewidth(3)
    stemlines.set_color("black")
    markerline.set_markersize(10)
    markerline.set_color("black")

    # And the back leg
    line_L = smoothLine(
        np.array(
            [
                [10, 0.0],
                [10, 0.1],
                [15, 0.3],
                [13, 0.5],
                [13, 0.6],
                [20, 0.7],
                [10, 0.8],
                [1, 0.9],
            ]
        ),
        horizontal=False,
        n=25,
    )
    markerline, stemlines, baseline = ax_4CL.stem(
        line_L[:20, 1],
        line_L[:20, 0],
        orientation="horizontal",
        bottom=0,
        linefmt="-",
        markerfmt="o",
        basefmt=" ",
    )
    stemlines.set_linewidth(4)
    stemlines.set_color(colours["blue"])
    markerline.set_markersize(15)
    markerline.set_color(colours["blue"])
    markerline, stemlines, baseline = ax_4CL.stem(
        line_L[20:, 1],
        line_L[20:, 0],
        orientation="horizontal",
        bottom=0,
        linefmt="-",
        markerfmt="o",
        basefmt=" ",
    )
    stemlines.set_linewidth(4)
    stemlines.set_color(colours["blue"])
    markerline.set_markersize(0)
    markerline.set_color(colours["blue"])

    return ax_4CL
