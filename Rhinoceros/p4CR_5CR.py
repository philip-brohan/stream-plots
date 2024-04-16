# function to plot the contents of the row 4 and 5 Centre-Right panel

from utils import smoothLine, colours, viridis
import numpy as np
from scipy.stats.qmc import PoissonDisk
import matplotlib
import matplotlib.patches as patches


def p4CR_5CR(fig, gspec):
    ax_4CR_5CR = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_4CR_5CR.set_facecolor(colours["transparent"])
    ax_4CR_5CR.spines["right"].set_visible(False)
    ax_4CR_5CR.spines["top"].set_visible(False)

    # Make ground shadow with barbs
    engine = PoissonDisk(d=2, radius=0.02)
    points = engine.fill_space()
    x = points[:, 0] * 110 - 5
    y = points[:, 1] * 1.1 - 0.05
    # Trim above ground level
    wh = np.where(y < (0.45 + (100 - x) * 0.15 / 100))
    x = x[wh]
    y = y[wh]
    # Random amplitudes - all pointing SW
    a = np.random.random(x.shape[0]) * 100
    # Plot the barbs - light shading
    ax_4CR_5CR.barbs(
        x,
        y,
        a * -1,
        a * -1,
        barbcolor="black",
        flagcolor="black",
        length=7,
        linewidth=1.5,
        alpha=0.1,
    )
    # Trim ahead of hooves
    wh = np.where(y > (0.4 - (100 - x) * 0.4 / 70))
    x = x[wh]
    y = y[wh]
    a = a[wh]
    # Plot the barbs - heavy shading
    ax_4CR_5CR.barbs(
        x,
        y,
        a * -1,
        a * -1,
        barbcolor="black",
        flagcolor="black",
        length=7,
        linewidth=1.5,
        alpha=0.3,
    )

    # Patch for the left leg
    ll_b = smoothLine(
        np.array([[0, 0.1], [20, 0.07], [30, 0.06], [42, 0.07]]),
        horizontal=True,
    )
    ll_r = smoothLine(
        np.array(
            [
                [42, 0.07],
                [42, 0.2],
                [35, 0.3],
                [25, 0.35],
                [22, 0.4],
                [25, 0.6],
                [35, 0.7],
                [40, 0.95],
                [42, 1.0],
            ]
        ),
        horizontal=False,
    )
    ll_L = np.append(ll_b, ll_r, axis=0)
    llP = np.append(ll_L, [[0, 1]], axis=0)
    ll_patch = matplotlib.patches.Polygon(
        llP,
        facecolor=colours["background"],
        edgecolor=colours["blue"],
        linewidth=3,
        zorder=200,
    )
    ax_4CR_5CR.add_patch(ll_patch)
    # Fill in with vertical lines
    vl = ax_4CR_5CR.vlines(
        np.linspace(0, 42, 20),
        0,
        0.89,
        colors=viridis(np.random.rand(20) / 2 + 0.35),
        linestyles="solid",
        zorder=250,
    )
    vl.set_clip_path(ll_patch)
    vl.set_linewidth(2)
    # Add the cuff at the top
    vl = ax_4CR_5CR.vlines(
        np.linspace(0, 42, 8),
        0.9,
        1.0,
        colors=colours["purple"],
        linestyles="solid",
        zorder=250,
    )
    vl.set_clip_path(ll_patch)
    vl.set_linewidth(15)

    # Patch for the right leg
    rl_l = smoothLine(
        np.array([[20, 1], [20, 0.5], [30, 0.3], [40, 0.2]]),
        horizontal=False,
    )
    rl_b = smoothLine(
        np.array([[40, 0.2], [60, 0.18], [75, 0.2]]),
        horizontal=True,
        k=2,
    )
    rl_r = smoothLine(
        np.array(
            [
                [75, 0.2],
                [70, 0.4],
                [60, 0.45],
                [55, 0.5],
                [53, 0.55],
                [55, 0.6],
                [60, 0.75],
                [70, 0.85],
                [75, 1.0],
            ]
        ),
        horizontal=False,
        k=2,
    )
    rl_L = np.append(rl_l, rl_b, axis=0)
    rl_L = np.append(rl_L, rl_r, axis=0)
    rl_patch = matplotlib.patches.Polygon(
        rl_L,
        facecolor=colours["background"],
        edgecolor=colours["purple"],
        linewidth=3,
        zorder=100,
    )
    ax_4CR_5CR.add_patch(rl_patch)
    # Fill in with horizontal lines
    hl = ax_4CR_5CR.hlines(
        np.linspace(0.18, 1, 60),
        20,
        85,
        colors=viridis(np.random.rand(20) / 2 + 0.15),
        linestyles="solid",
        zorder=150,
    )
    hl.set_clip_path(rl_patch)
    hl.set_linewidth(2)

    # Eliptical patches for the dangling breastplate
    ep1 = patches.Ellipse(
        (75, 1.1),
        30,
        0.75,
        facecolor=viridis(0.5),
        edgecolor="black",
        linewidth=0,
        zorder=300,
    )
    ax_4CR_5CR.add_patch(ep1)
    ep2 = patches.Ellipse(
        (75, 1.1),
        20,
        0.4,
        facecolor=viridis(0.3),
        edgecolor="black",
        linewidth=0,
        zorder=350,
    )
    ax_4CR_5CR.add_patch(ep2)

    return ax_4CR_5CR
