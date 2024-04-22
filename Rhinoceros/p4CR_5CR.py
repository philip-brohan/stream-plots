# function to plot the contents of the row 4 and 5 Centre-Right panel

from utils import smoothLine, colours, viridis
import numpy as np
from scipy.stats.qmc import PoissonDisk
import matplotlib
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection


def p4CR_5CR(fig, gspec):
    ax_4CR_5CR = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[10, 30, 50, 70, 90],
        ylim=[0, 1],
        yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
        yticklabels=["0", "0.2", "0.4", "0.6", "0.8", "1"],
    )
    ax_4CR_5CR.set_facecolor(colours["ax_bg"])
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
        np.array([[-5, 0.1], [20, 0.07], [30, 0.06], [42, 0.07]]),
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
                [40, 0.87],
            ]
        ),
        horizontal=False,
    )
    ll_L = np.append(ll_b, ll_r, axis=0)
    llP = np.append(ll_L, [[-5, 0.87]], axis=0)
    ll_patch = matplotlib.patches.Polygon(
        llP,
        facecolor="none",
        edgecolor="none",
        linewidth=0,
        zorder=200,
    )
    ax_4CR_5CR.add_patch(ll_patch)
    # Fill with rectangular patches
    engine = PoissonDisk(d=2, radius=0.03)
    points = engine.fill_space()
    x = points[:, 0] * 100 - 10
    y = points[:, 1] * 1.1 - 0.05
    # Trim to the leg patch
    path = ll_patch.get_path()
    transformed_path = path.transformed(ll_patch.get_patch_transform())
    inside = transformed_path.contains_points(np.column_stack((x, y)))
    x = x[inside]
    y = y[inside]
    c = np.random.rand(x.shape[0]) / 4 + 0.6
    # Create a patch at every point
    ptch = []
    for (
        x1,
        y1,
        c1,
    ) in zip(x, y, c):
        square = patches.Rectangle(
            (x1, y1),
            7,
            0.06,
            facecolor=viridis(c1),
            edgecolor=viridis(1.0),
            linewidth=2,
            zorder=220 + 100 * y1,
        )
        ax_4CR_5CR.add_patch(square)

    # Add the cuff at the top
    vl = ax_4CR_5CR.vlines(
        np.linspace(0, 42, 8),
        0.9,
        1.0,
        colors=colours["purple"],
        linestyles="solid",
        zorder=350,
    )
    vl.set_linewidth(15)
    vl = ax_4CR_5CR.vlines(
        np.linspace(4, 46, 8),
        0.9,
        1.0,
        colors=colours["yellow"],
        linestyles="solid",
        zorder=340,
    )
    vl.set_linewidth(20)

    # Patch for the right leg
    rl_l = smoothLine(
        np.array([[42, 1], [42, 0.8], [20, 0.5], [30, 0.3], [40, 0.2]]),
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
        facecolor="none",
        edgecolor="none",
        linewidth=0,
        zorder=100,
    )
    ax_4CR_5CR.add_patch(rl_patch)
    # Fill with circular patches
    engine = PoissonDisk(d=2, radius=0.03)
    points = engine.fill_space()
    x = points[:, 0] * 110 - 5
    y = points[:, 1] * 1.1 - 0.05
    # Trim to the leg patch
    path = rl_patch.get_path()
    transformed_path = path.transformed(rl_patch.get_patch_transform())
    inside = transformed_path.contains_points(np.column_stack((x, y)))
    x = x[inside]
    y = y[inside]
    c = np.random.rand(x.shape[0]) / 4 + 0.25
    # Create a patch at every point
    ptch = []
    for (
        x1,
        y1,
        c1,
    ) in zip(x, y, c):
        circle = patches.Ellipse(
            (x1, y1),
            7,
            0.06,
            facecolor=viridis(c1),
            edgecolor=viridis(0),
            linewidth=2,
            zorder=120 + 100 * y1,
        )
        ax_4CR_5CR.add_patch(circle)

    # Eliptical patches for the dangling breastplate
    ep1 = patches.Ellipse(
        (75, 1.1),
        30,
        0.75,
        facecolor=viridis(0.5),
        edgecolor=viridis(1.0),
        linewidth=5,
        zorder=300,
    )
    ax_4CR_5CR.add_patch(ep1)
    ep2 = patches.Ellipse(
        (75, 1.1),
        20,
        0.4,
        facecolor=viridis(0.3),
        edgecolor=viridis(0.0),
        linewidth=3,
        zorder=350,
    )
    ax_4CR_5CR.add_patch(ep2)

    return ax_4CR_5CR
