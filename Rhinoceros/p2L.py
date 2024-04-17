# function to plot the contents of the row 2 Left panel

from utils import smoothLine, colours, viridis
import numpy as np
import matplotlib


def p2L(fig, gspec):
    ax_2L = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[0, 20, 40, 60, 80, 100],
        ylim=[0, 1],
        yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
    )
    ax_2L.set_facecolor(colours["ax_bg"])
    ax_2L.spines["right"].set_visible(False)
    ax_2L.spines["top"].set_visible(False)

    # Grid of points for quiver locations
    x = np.linspace(0, 100, 60)
    y = np.linspace(0, 1, 40)
    X, Y = np.meshgrid(x, y)

    # Outline of back plate
    backl_2L = smoothLine(
        np.array(
            [
                [17, 0.0],
                [17, 0.05],
                [19, 0.25],
                [20, 0.55],
                [25, 0.75],
                [30, 0.95],
                [32, 1.00],
            ]
        ),
        horizontal=False,
    )
    # Close the polygon by inserting elements outside of the axes window
    backl_2L = np.append(backl_2L, [[100, 1.0], [100, 0.0]], axis=0)
    back_patch = matplotlib.patches.Polygon(
        backl_2L, facecolor=colours["background"], edgecolor="none", zorder=10
    )
    ax_2L.add_patch(back_patch)

    # Fill back patch with random direction quivers
    U = np.random.rand(X.shape[0], X.shape[1]) - 0.5
    V = np.random.rand(X.shape[0], X.shape[1]) - 0.5
    M = np.hypot(U, V)
    U /= M
    V /= M
    U = X.copy() * 0.0 + 1.0
    V = Y.copy() * 0.0
    ax_2L.quiver(
        X,
        Y,
        U * 1.414,
        V * 1.414,
        color=colours["purple"],
        scale_units="y",
        scale=20,  # Arrow length 1/20 of y axis units
        units="y",
        width=0.01,  # Arrow width 0.01 of y axis units
        zorder=20,
        clip_path=back_patch,
    )

    # Fewer arrows for the front plates
    x = np.linspace(0, 100, 30)
    y = np.linspace(0, 1, 20)
    X, Y = np.meshgrid(x, y)

    # Outline of hip plate
    hipl_2L = smoothLine(
        np.array(
            [[15, -0.1], [19, 0.0], [30, 0.15], [50, 0.22], [70, 0.10], [90, -0.1]]
        ),
        horizontal=True,
    )
    hip_patch = matplotlib.patches.Polygon(
        hipl_2L, facecolor=colours["background"], edgecolor="none", zorder=50
    )
    ax_2L.add_patch(hip_patch)

    # Fill hip patch with NE-pointing quivers
    ax_2L.quiver(
        X,
        Y,
        1,
        1,
        color=colours["green"],
        scale_units="y",
        scale=20,  # Arrow length 1/20 of y axis units
        units="y",
        width=0.01,  # Arrow width 0.01 of y axis units
        zorder=100,
        clip_path=hip_patch,
    )

    # Outline of top plate
    topl_2L = smoothLine(
        np.array(
            [
                [110, 0.2],
                [80, 0.22],
                [60, 0.25],
                [40, 0.3],
                [25, 0.4],
                [15, 0.6],
                [20, 0.65],
                [30, 0.75],
                [40, 0.9],
                [50, 1.05],
            ]
        ),
        horizontal=False,
    )
    # Close the polygon by inserting elements outside of the axes window
    topl_2L = np.append(topl_2L, [[110, 1.05]], axis=0)
    top_patch = matplotlib.patches.Polygon(
        topl_2L, facecolor=colours["background"], edgecolor="none", zorder=30
    )
    ax_2L.add_patch(top_patch)

    # Fill top plate with SW-pointing quivers
    ax_2L.quiver(
        X,
        Y,
        -1,
        -1,
        color=colours["blue"],
        scale_units="y",
        scale=20,  # Arrow length 1/20 of y axis units
        units="y",
        width=0.01,  # Arrow width 0.01 of y axis units
        zorder=40,
        clip_path=top_patch,
    )

    # Outline of belly plate
    belly_2L = smoothLine(
        np.array([[78, -0.1], [75, 0], [73, 0.25], [78, 0.65], [90, 1], [100, 1.1]]),
        horizontal=False,
    )
    # Close the polygon by inserting elements outside of the axes window
    belly_2L = np.append(belly_2L, [[110, 1.1], [110, -0.1]], axis=0)
    belly_patch = matplotlib.patches.Polygon(
        belly_2L,
        facecolor=colours["ax_bg"],
        edgecolor="none",
        linewidth=0,
        zorder=200,
    )
    ax_2L.add_patch(belly_patch)
    xy = np.array(
        [
            [80, 0.25],
            [80, 0.12],
            [83, 0.58],
            [86, 0.35],
            [89, 0.4],
            [92, 0.10],
            [95, 0.85],
            [98, 0.50],
            [95, 0.28],
            [90, 0.70],
        ]
    )
    bplot = ax_2L.boxplot(
        np.random.rand(25, xy.shape[0]) / 5 + xy[:, 1],
        positions=xy[:, 0],
        widths=6,
        manage_ticks=False,
        patch_artist=True,  # fill with color
        showmeans=False,
        showfliers=False,
        medianprops={"color": "black", "linewidth": 2},
        boxprops={"facecolor": "black", "edgecolor": "black", "linewidth": 2},
        whiskerprops={"color": "black", "linewidth": 3},
        capprops={"color": "black", "linewidth": 3},
        zorder=400,
    )
    colors = viridis(xy[:, 1] / 2 + 0.5)
    for patch, color in zip(bplot["boxes"], colors):
        patch.set_facecolor(color)
    for key in bplot.keys():
        for element in bplot[key]:
            element.set_clip_path(belly_patch)

    return ax_2L
