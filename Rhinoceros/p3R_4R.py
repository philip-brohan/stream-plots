# function to plot the contents of the row 3 and 4 Right panel

from utils import smoothLine, colours, viridis
import numpy as np
import sys


def p3R_4R(fig, gspec, bg_im, bgi_extent):
    ax_3R_4R = fig.add_subplot(
        gspec,
        frameon=True,
        xlim=[0, 100],
        xticks=[10, 30, 50, 70, 90],
        ylim=[0, 1],
        yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
        yticklabels=["0", "0.2", "0.4", "0.6", "0.8", "1"],
    )
    ax_3R_4R.set_facecolor(colours["ax_bg"])
    ax_3R_4R.spines["right"].set_visible(False)
    ax_3R_4R.spines["top"].set_visible(False)

    # Get the background image array section that fills this axes
    bbox = ax_3R_4R.get_position()
    im_sh = bg_im.shape
    x0 = int((bbox.x0 - bgi_extent[0]) / (bgi_extent[1] - bgi_extent[0]) * im_sh[1])
    x1 = int((bbox.x1 - bgi_extent[0]) / (bgi_extent[1] - bgi_extent[0]) * im_sh[1])
    y0 = int((bbox.y0 - bgi_extent[2]) / (bgi_extent[3] - bgi_extent[2]) * im_sh[0])
    y1 = int((bbox.y1 - bgi_extent[2]) / (bgi_extent[3] - bgi_extent[2]) * im_sh[0])
    bg_im_f = np.flip(bg_im, axis=0)  # flip the image array to match the axes direction
    im_in_ax = bg_im_f[max(y0, 0) : min(y1, im_sh[0]), max(x0, 0) : min(x1, im_sh[1])]
    # Pad if axes extend beyond the image array
    if x0 < 0:
        im_in_ax = np.insert(
            im_in_ax,
            0,
            np.full([im_in_ax.shape[0], -x0, im_in_ax.shape[2]], 1.0),
            axis=1,
        )
    if x1 > im_sh[1]:
        im_in_ax = np.append(
            im_in_ax,
            np.full([im_in_ax.shape[0], x1 - im_sh[1], im_in_ax.shape[2]], 1.0),
            axis=1,
        )
    if y0 < 0:
        im_in_ax = np.insert(
            im_in_ax,
            0,
            np.full([-y0, im_in_ax.shape[1], im_in_ax.shape[2]], 1.0),
            axis=0,
        )
    if y1 > im_sh[0]:
        im_in_ax = np.append(
            im_in_ax,
            np.full([y1 - im_sh[0], im_in_ax.shape[1], im_in_ax.shape[2]], 1.0),
            axis=0,
        )
    # Image to greyscale
    im_in_ax = np.mean(im_in_ax, axis=2)
    # Threshold the image
    im_in_ax[im_in_ax > 0.5] = 1.0
    im_in_ax[im_in_ax != 1.0] = 0.0
    # Convert to a set of non-zero xy points

    x = np.linspace(0, 100, im_in_ax.shape[1])
    y = np.linspace(0, 1, im_in_ax.shape[0])
    X, Y = np.meshgrid(x, y)
    x = X[im_in_ax == 0.0]
    y = Y[im_in_ax == 0.0]
    # Plot as 2d histogram
    ax_3R_4R.hist2d(
        x,
        y,
        bins=[20, 10],
        cmin=0.05,
        range=[[0, 100], [0, 1]],
        cmap=viridis.reversed(),
        alpha=1,
    )
    # Add a highlight for the eye
    ax_3R_4R.plot(
        39,
        0.55,
        color=colours["yellow"],
        marker="o",
        markersize=35,
        alpha=1,
    )
    ax_3R_4R.plot(
        39,
        0.55,
        color=colours["blue"],
        marker="o",
        markersize=15,
        alpha=1,
    )
    return ax_3R_4R
