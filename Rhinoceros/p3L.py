# function to plot the contents of the row 3 Left panel

from utils import smoothLine, colours, viridis
import numpy as np


def p3L(fig, gspec):
    ax_3L = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_3L.set_facecolor(colours["transparent"])
    ax_3L.spines["right"].set_visible(False)
    ax_3L.spines["top"].set_visible(False)
    xp = np.random.rand(5000) * 2
    yp = np.random.rand(5000) * 2
    radius = ((1 - xp) ** 2 + (1 - yp) ** 2) ** 0.5
    xp = xp[radius < 0.5]
    yp = yp[radius < 0.5]
    ax_3L.hexbin(
        (xp - 0.35) * 100,
        (yp - 0.6) * 1.5,
        gridsize=15,
        mincnt=1,
        cmap=viridis,
        edgecolors="white",
        alpha=0.5,
        zorder=100,
    )
    # Polygon points matched to original
    poly_3L = smoothLine(
        np.array([[73, 1.1], [75, 1], [80, 0.7], [90, 0.3], [100, 0.1], [110, 0.1]])
    )
    # Draw the line to be a shadow effect
    ax_3L.plot(
        poly_3L[:, 0],
        poly_3L[:, 1],
        color=(0, 0, 0, 0.1),
        linewidth=5,
        marker="none",
        zorder=200,
    )
    # Close the polygon by inserting elements outside of the axes window
    poly_3L = np.append(poly_3L, [[110, 1.1], [73, 1.1]], axis=0)
    ax_3L.fill_between(
        poly_3L[:, 0],
        poly_3L[:, 1],
        color=colours["background"],
        edgecolor="none",
        zorder=300,
    )
    x = [80, 85, 90, 95, 93, 97, 95, 92]
    y = [0.95, 0.7, 0.4, 0.25, 0.8, 0.49, 0.9, 0.6]
    xe = [4, 5, 3, 3, 6, 2, 2, 2]
    ye = [0.15, 0.14, 0.1, 0.08, 0.05, 0.15, 0.05, 0.05]
    color = viridis(np.random.rand(len(x)))
    for idx in range(len(x)):
        ax_3L.errorbar(
            x[idx],
            y[idx],
            xerr=xe[idx],
            yerr=ye[idx],
            fmt="none",
            ecolor=color[idx],
            capsize=5,
            elinewidth=3,
            capthick=3,
            zorder=400,
        )

    return ax_3L
