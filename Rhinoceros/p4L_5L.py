# function to plot the contents of the row 4 and 5 Left panel

import sys
from matplotlib.patches import Polygon
from utils import smoothLine, colours, viridis
import numpy as np
import matplotlib


def p4L_5L(fig, gspec):
    ax_4L_5L = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_4L_5L.set_facecolor(colours["ax_bg"])
    ax_4L_5L.spines["right"].set_visible(False)
    ax_4L_5L.spines["top"].set_visible(False)

    # Bottom of the hip plate
    hipl = smoothLine(
        np.array(
            [
                [20, 1.0],
                [30, 0.8],
                [50, 0.65],
                [70, 0.55],
                [80, 0.65],
                [90, 0.72],
                [100, 1.0],
            ]
        ),
        horizontal=True,
        k=3,
    )
    hip_patch = matplotlib.patches.Polygon(
        hipl, facecolor=colours["ax_bg"], edgecolor="none", zorder=200
    )
    ax_4L_5L.add_patch(hip_patch)

    # Fill the hip patch with a streamplot
    # make a stream function:
    X, Y = np.meshgrid(np.linspace(0, 100, 200), np.linspace(0, 1, 200))
    Z = ((X - 60) / 10) ** 3 + (100 * (Y - 0.7)) ** 2
    # make U and V out of the streamfunction:
    V = np.diff(Z[1:, :], axis=1)
    U = -np.diff(Z[:, 1:], axis=0)
    sps = ax_4L_5L.streamplot(
        X[1:, 1:],
        Y[1:, 1:],
        U,
        V,
        arrowsize=0,  # Arrows can't be clipped - they will be drawn outside the hip patch
        density=2,
        linewidth=3,
        color=colours["purple"],
        zorder=250,
    )
    sps.lines.set_clip_path(hip_patch)

    # Rear right leg
    legr_l = smoothLine(  # Left side
        np.array(
            [
                [30, 0.85],
                [18, 0.65],
                [23, 0.3],
                [20, 0.22],
                [28, 0.1],
            ]
        ),
        horizontal=False,
    )
    legr_b = smoothLine(  # Bottom
        np.array(
            [
                [28, 0.1],
                [40, 0.06],
                [60, 0.05],
                [78, 0.08],
            ]
        ),
        horizontal=True,
        k=2,
    )
    legr_r = smoothLine(  # Right side
        np.array(
            [
                [78, 0.08],
                [70, 0.25],
                [60, 0.3],
                [55, 0.35],
                [60, 0.5],
                [65, 0.6],
            ]
        ),
        horizontal=False,
        k=2,
    )
    legr = np.append(legr_l, legr_b, axis=0)
    legr = np.append(legr, legr_r, axis=0)
    legr_patch = matplotlib.patches.Polygon(
        legr,
        facecolor=colours["ax_bg"],
        edgecolor=colours["green"],
        hatch="X",
        linewidth=3,
        zorder=100,
    )
    ax_4L_5L.add_patch(legr_patch)

    # Rear left leg
    legl = smoothLine(
        np.array(
            [
                [100, 0.25],
                [95, 0.4],
                [90, 0.45],
                [80, 0.65],
                [70, 0.8],
                [85, 0.9],
                [100, 1.0],
            ]
        ),
        horizontal=False,
        k=2,
    )
    legl_patch = matplotlib.patches.Polygon(
        legl,
        facecolor=colours["ax_bg"],
        edgecolor=colours["blue"],
        hatch="//",
        linewidth=3,
        zorder=20,
    )
    ax_4L_5L.add_patch(legl_patch)

    # Ground shading with a clipped gradient
    phi = 0.5 * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]], [v @ [0, 0], v @ [0, 1]]])
    a, b = (0, 1)
    X = a + (b - a) / X.max() * X
    im = ax_4L_5L.imshow(
        X,
        interpolation="bicubic",
        clim=(0, 1),
        aspect="auto",
        extent=(100, 0, 0, 1),
        cmap="gray_r",
        alpha=0.3,
        zorder=5,
    )
    im.set_clip_path(
        Polygon([[0, 0], [0, 0.4], [100, 0.6], [100, 0]], transform=ax_4L_5L.transData)
    )

    # bottom part of tail
    yt = np.linspace(10, 15, 8)
    lengths = 0.07  # + np.random.rand(yt.shape[0]) * 0.1
    ax_4L_5L.vlines(
        yt,
        ymin=1.0 - lengths,
        ymax=1.0,
        colors=colours["blue"],
        linewidths=1,
        zorder=10,
    )
    yt = np.linspace(8, 10, 3)
    lengths = np.random.rand(yt.shape[0]) * 0.05 + 0.05
    ax_4L_5L.vlines(
        yt,
        ymin=0.95 - lengths,
        ymax=0.95,
        colors=colours["blue"],
        linewidths=1,
        zorder=10,
    )
    yt = np.linspace(15, 17, 3)
    lengths = np.random.rand(yt.shape[0]) * 0.05 + 0.05
    ax_4L_5L.vlines(
        yt,
        ymin=0.95 - lengths,
        ymax=0.95,
        colors=colours["blue"],
        linewidths=1,
        zorder=10,
    )

    return ax_4L_5L
