# function to plot the contents of the row 2 Centre Right panel

from utils import smoothLine, colours, viridis
import numpy as np
import matplotlib
from scipy.ndimage import gaussian_filter
from scipy.stats.qmc import PoissonDisk


def p2CR(fig, gspec):
    ax_2CR = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_2CR.set_facecolor(colours["ax_bg"])
    ax_2CR.spines["right"].set_visible(False)
    ax_2CR.spines["top"].set_visible(False)

    # Make a data grid to cover the axes
    x = np.linspace(0, 100, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)

    # Shoulder plate
    Z = np.sqrt(X**2 + (80 * Y) ** 2)
    Z[Z > 70] = 70
    Z = Z - 70
    Z /= 2
    Z = Z * -1
    Z[Z > 10] = 10

    # Add point rises to the shoulder plate
    engine = PoissonDisk(d=2, radius=0.1)
    points = engine.fill_space()
    x = points[:, 0] * 100
    y = points[:, 1] * 100
    r = np.sqrt(x**2 + (y * 0.8) ** 2)
    x = x[r < 50].astype(int)
    y = y[r < 50].astype(int)
    Z[y, x] += 200
    Z = gaussian_filter(Z, 2)

    # Neck plate - rectangular
    cpx = 85  # centre point
    cpy = 0.5
    dx = np.abs((X - cpx) * 1.0 + (Y - cpy) * 100 * 0.6)
    dy = np.abs((X - cpx) * 0.6 - (Y - cpy) * 100 * 1.0) * 0.75
    Z2 = np.maximum(dx, dy)
    Z2[Z2 > 25] = 25
    Z2 = (Z2 - 25) * -1

    # Top plate - trianguar
    cpx = 55  # centre point
    cpy = 1.0
    dx = np.abs((X - cpx) * 1.0 + (Y - cpy) * 100 * 0.6)
    dy = np.abs((X - cpx) * 1.0 - (Y - cpy) * 100 * 1.0) * 0.75
    Z3 = np.maximum(dx, dy)
    Z3[Z3 > 25] = 25
    Z3 = (Z3 - 25) * -1

    # Contour plot
    contour = ax_2CR.contour(
        X, Y, Z + Z2 + Z3, levels=15, cmap=viridis, linewidths=4, zorder=250
    )

    return ax_2CR
