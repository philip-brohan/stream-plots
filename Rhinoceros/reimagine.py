#!/usr/bin/env python

# Re-draw Durer's Rhinecerous using Matplotlib

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from PIL import Image
import numpy as np

# Load the original
im = Image.open(r"The_Rhinoceros_(NGA_1964.8.697)_enhanced.png")
im = im.convert("RGB")
# Convert to numpy array on 0-1
im = np.array(im) / 255.0

# Figure showing the original image, reconstructed image, and latent space
fig = Figure(
    figsize=(3000 / 100, 2368 / 100),  # Width, Height (inches)
    dpi=300,
    facecolor=(0.95, 0.95, 0.95, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=True,
    subplotpars=None,
    tight_layout=None,
)
canvas = FigureCanvas(fig)
font = {"family": "sans-serif", "sans-serif": "Arial", "weight": "normal", "size": 18}
matplotlib.rc("font", **font)

# Put image in as background
axb = fig.add_axes([0, 0, 1, 1])
axb.set_axis_off()
axb.set_xlim(0, 1)
axb.set_ylim(0, 1)
# Add the image
axb.imshow(im, extent=[0.03, 0.98, 0.03, 0.98], aspect="auto", alpha=0.5)

# Add a grid of axes
gspec = matplotlib.gridspec.GridSpec(
    ncols=4,
    nrows=5,
    figure=fig,
    width_ratios=[
        1.5,
        1.5,
        1.5,
        1.5,
    ],
    height_ratios=[1, 1, 1, 1, 1],
    wspace=0.1,
    hspace=0.1,
)
# Set the space the subplots take up
fig.subplots_adjust(left=0.02, right=0.99, bottom=0.02, top=0.9)

# Each subplot is different

# Top Left
ax_TL = fig.add_subplot(
    gspec[0, 0],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_TL.set_facecolor((1, 1, 1, 0.5))
ax_TL.spines["right"].set_visible(False)
ax_TL.spines["top"].set_visible(False)

# Top Centre Left
ax_TCL = fig.add_subplot(
    gspec[0, 1],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_TCL.set_facecolor((1, 1, 1, 0.5))
ax_TCL.spines["right"].set_visible(False)
ax_TCL.spines["top"].set_visible(False)

# Top Right and Centre Right
ax_TCR_TR = fig.add_subplot(
    gspec[0, 2:4],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_TCR_TR.set_facecolor((1, 1, 1, 0.5))
ax_TCR_TR.spines["right"].set_visible(False)
ax_TCR_TR.spines["top"].set_visible(False)

# 2nd Left
ax_2L = fig.add_subplot(
    gspec[1, 0],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_2L.set_facecolor((1, 1, 1, 0.5))
ax_2L.spines["right"].set_visible(False)
ax_2L.spines["top"].set_visible(False)

# 2nd and 3rd Centre Left
ax_23CL = fig.add_subplot(
    gspec[1:3, 1],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_23CL.set_facecolor((1, 1, 1, 0.5))
ax_23CL.spines["right"].set_visible(False)
ax_23CL.spines["top"].set_visible(False)

# 2nd Centre Right
ax_2CR = fig.add_subplot(
    gspec[1, 2],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_2CR.set_facecolor((1, 1, 1, 0.5))
ax_2CR.spines["right"].set_visible(False)
ax_2CR.spines["top"].set_visible(False)

# 2nd Right
ax_2R = fig.add_subplot(
    gspec[1, 3],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_2R.set_facecolor((1, 1, 1, 0.5))
ax_2R.spines["right"].set_visible(False)
ax_2R.spines["top"].set_visible(False)

# 3rd Left
ax_3L = fig.add_subplot(
    gspec[2, 0],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_3L.set_facecolor((1, 1, 1, 0.5))
ax_3L.spines["right"].set_visible(False)
ax_3L.spines["top"].set_visible(False)

# 3rd Centre Right
ax_3CR = fig.add_subplot(
    gspec[2, 2],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_3CR.set_facecolor((1, 1, 1, 0.5))
ax_3CR.spines["right"].set_visible(False)
ax_3CR.spines["top"].set_visible(False)

# 3rd and 4th Right
ax_34R = fig.add_subplot(
    gspec[2:4, 3],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_34R.set_facecolor((1, 1, 1, 0.5))
ax_34R.spines["right"].set_visible(False)
ax_34R.spines["top"].set_visible(False)

# 4th and 5th Left
ax_45L = fig.add_subplot(
    gspec[3:5, 0],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_45L.set_facecolor((1, 1, 1, 0.5))
ax_45L.spines["right"].set_visible(False)
ax_45L.spines["top"].set_visible(False)

# 4th Centre Left
ax_4CL = fig.add_subplot(
    gspec[3, 1],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_4CL.set_facecolor((1, 1, 1, 0.5))
ax_4CL.spines["right"].set_visible(False)
ax_4CL.spines["top"].set_visible(False)

# 4th and 5th Centre Right
ax_45CR = fig.add_subplot(
    gspec[3:5, 2],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_45CR.set_facecolor((1, 1, 1, 0.5))
ax_45CR.spines["right"].set_visible(False)
ax_45CR.spines["top"].set_visible(False)

# 5th Centre Left
ax_5CL = fig.add_subplot(
    gspec[4, 1],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_5CL.set_facecolor((1, 1, 1, 0.5))
ax_5CL.spines["right"].set_visible(False)
ax_5CL.spines["top"].set_visible(False)

# 5th Right
ax_5R = fig.add_subplot(
    gspec[4, 3],
    frameon=True,
    xlim=[0, 100],
    xticks=[0, 20, 40, 60, 80, 100],
    ylim=[0, 1],
    yticks=[0.1, 0.3, 0.5, 0.7, 0.9],
)
ax_5R.set_facecolor((1, 1, 1, 0.5))
ax_5R.spines["right"].set_visible(False)
ax_5R.spines["top"].set_visible(False)


# Render the new image
fig.savefig("reimagine.webp")
