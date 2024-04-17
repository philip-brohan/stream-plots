# function to plot the contents of the row 5 Centre-Left panel

from utils import smoothLine, colours
import numpy as np
import scipy.stats as sps
import matplotlib


def p5CL(fig, gspec):
    ax_5CL = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 100],
        yticks=[10, 30, 50, 70, 90],
    )
    ax_5CL.set_facecolor(colours["ax_bg"])
    ax_5CL.spines["right"].set_visible(False)
    ax_5CL.spines["top"].set_visible(False)

    # Use a grid to imitate the shading shadow
    yd = sps.norm(loc=0.6, scale=0.2).ppf(np.linspace(0.01, 0.99, 50))
    xd = sps.norm(loc=100, scale=15).ppf(np.linspace(0.01, 0.5, 50))
    ax_5CL.set_yticks(yd[yd < 1] * 100, minor=True)
    ax_5CL.set_xticks(xd, minor=True)
    ax_5CL.grid(
        visible=True,
        which="minor",
        axis="both",
        color="black",
        linestyle="-",
        linewidth=0.25,
    )

    # Outline of rear-left foot
    footl = smoothLine(
        np.array([[45, 60], [40, 90], [30, 100]]),
        horizontal=False,
        k=2,
    )
    # Flat bottom of foot
    footl = np.append([[0, 45], [40, 45]], footl, axis=0)
    # Close the polygon by inserting elements outside of the axes window
    footl = np.append(footl, [[0, 100]], axis=0)
    foot_patch = matplotlib.patches.Polygon(
        footl,
        facecolor=colours["ax_bg"],
        edgecolor=colours["blue"],
        linewidth=2,
        zorder=100,
    )
    ax_5CL.add_patch(foot_patch)
    # Make a sparse data grid to cover the axes
    Z = np.random.rand(100, 100)
    Z[Z < 0.6] = 0
    ax_5CL.spy(
        Z,
        zorder=150,
        aspect="auto",
        markersize=2,
        color=colours["blue"],
        origin="lower",
        clip_path=foot_patch,
    )

    return ax_5CL
