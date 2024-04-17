# function to plot the contents of the rows 2 and 3 and Centre-Left panel

from utils import smoothLine, colours, viridis
import numpy as np


def p2CL_3CL(fig, gspec):
    ax_2CL_3CL = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[10, 30, 50, 70, 90],
        ylim=[0, 1],
        yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
        yticklabels=["0", "0.2", "0.4", "0.6", "0.8", "1"],
    )
    ax_2CL_3CL.set_facecolor(colours["ax_bg"])
    ax_2CL_3CL.spines["right"].set_visible(False)
    ax_2CL_3CL.spines["top"].set_visible(False)
    # Ribs as lines
    line_R1 = smoothLine(
        np.array(
            [
                [0, 0.8],
                [10, 0.95],
                [18, 1.0],
            ]
        ),
        horizontal=False,
        k=2,
    )
    ax_2CL_3CL.plot(line_R1[:, 0], line_R1[:, 1], c=colours["blue"], lw=10, alpha=1)
    line_R2 = smoothLine(
        np.array(
            [
                [20, 0.2],
                [10, 0.5],
                [25, 1.0],
            ]
        ),
        horizontal=False,
        k=2,
    )
    ax_2CL_3CL.plot(line_R2[:, 0], line_R2[:, 1], c=colours["blue"], lw=10, alpha=1)
    line_R3 = smoothLine(
        np.array(
            [
                [30, 0.3],
                [32, 0.65],
                [45, 1.0],
            ]
        ),
        horizontal=False,
        k=2,
    )
    ax_2CL_3CL.plot(line_R3[:, 0], line_R3[:, 1], c=colours["blue"], lw=10, alpha=1)
    line_R4 = smoothLine(
        np.array(
            [
                [60, 0.3],
                [65, 0.65],
                [60, 1.0],
            ]
        ),
        horizontal=False,
        k=2,
    )
    ax_2CL_3CL.plot(line_R4[:, 0], line_R4[:, 1], c=colours["blue"], lw=10, alpha=1)
    line_R5 = smoothLine(
        np.array(
            [
                [85, 0.5],
                [85, 0.7],
                [72, 1.0],
            ]
        ),
        horizontal=False,
        k=2,
    )
    ax_2CL_3CL.plot(line_R5[:, 0], line_R5[:, 1], c=colours["blue"], lw=10, alpha=1)
    line_R6 = smoothLine(
        np.array([[90, 0.9], [85, 0.95], [80, 1.0]]),
        horizontal=False,
        k=2,
    )
    ax_2CL_3CL.plot(line_R6[:, 0], line_R6[:, 1], c=colours["blue"], lw=10, alpha=1)
    # line of shadow from shoulder plate
    line_SS = smoothLine(
        np.array(
            [
                [92, 0.0],
                [88, 0.1],
                [85, 0.2],
                [85, 0.3],
                [86, 0.4],
                [90, 0.5],
                [94, 0.6],
                [100, 0.7],
            ]
        ),
        horizontal=False,
        k=2,
    )
    # ax_2CL_3CL.plot(line_SS[:, 0], line_SS[:, 1], c="black", lw=10, alpha=1)

    xy = np.array(
        [
            [5, 0.65],
            [3, 0.58],
            [4, 0.49],
            [5, 0.4],
            [2, 0.05],
            [5, 0.15],
            [5, 0.28],
            [12, 0.03],
            [12, 0.22],
            [15, 0.55],
            [25, 0.51],
            [20, 0.4],
            [12, 0.12],
            [17, 0.1],
            [22, -0.02],
            [28, 0.05],
            [22, 0.14],
            [20, 0.25],
            [27, 0.24],
            [33, 0.13],
            [38, 0.04],
            [42, 0.1],
            [37, 0.23],
            [50, 0.09],
            [47, 0.18],
            [55, 0.15],
            [59, 0.05],
            [72, 0.1],
            [69, 0.16],
            [80, 0.11],
            [78, 0.15],
            [76, 0.23],
            [82, 0.15],
            [80, 0.2],
            [76, 0.3],
            [35, 0.35],
            [45, 0.35],
            [47, 0.45],
            [40, 0.5],
            [52, 0.5],
            [50, 0.6],
            [45, 0.65],
            [55, 0.7],
            [70, 0.3],
            [75, 0.5],
            [75, 0.65],
        ]
    )
    # colors = viridis(np.random.rand(len(xy)))
    colors = viridis(xy[:, 1])
    size = 1000
    ax_2CL_3CL.scatter(xy[:, 0], xy[:, 1], c=colors, s=size, alpha=1)
    ax_2CL_3CL.scatter(
        xy[:, 0], xy[:, 1], color=colours["ax_bg"], s=size / 4, alpha=0.5
    )

    y = [
        0.05,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5,
        0.55,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
    ]
    x = [
        8,
        10,
        12,
        14,
        16,
        16,
        14,
        13,
        12,
        11,
        10,
        9,
        8,
        7,
        6,
        5,
        4,
        3,
    ]
    ax_2CL_3CL.barh(
        y=y,
        width=[i * -1 for i in x],
        left=100,
        height=0.04,
        color=viridis([1 - v for v in y]),
        alpha=1,
    )

    return ax_2CL_3CL
