#!/usr/bin/env python

# Re-draw Durer's Rhinecerous using Matplotlib

import sys
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Polygon

from PIL import Image
import numpy as np
from utils import smoothLine, viridis, colours

# Load the original
bg_im = Image.open(r"The_Rhinoceros_(NGA_1964.8.697)_enhanced.png")
bg_im = bg_im.convert("RGB")
# Convert to numpy array on 0-1
bg_im = np.array(bg_im) / 255.0

# Figure showing the original image, reconstructed image, and latent space
fig = Figure(
    figsize=(3000 / 100, 2368 / 100),  # Width, Height (inches)
    dpi=300,
    facecolor=colours["background"],
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
bgi_extent = [0.03, 0.98, 0.03, 0.98]
axb.imshow(bg_im, extent=bgi_extent, aspect="auto", alpha=0.5)

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


# Each subplot has a separate function to draw it

# Top Left
from pTL import pTL

# ax_TL = pTL(fig, gspec[0, 0])

# Top Centre Left
from pTCL import pTCL

# ax_TCL = pTCL(fig, gspec[0, 1])

# Top Right and Centre Right
from pTCR_TR import pTCR_TR

# ax_TCR_TR = pTCR_TR(fig, gspec[0, 2:4])

# 2nd Left
from p2L import p2L

ax_2L = p2L(fig, gspec[1, 0])

# 2nd and 3rd Centre Left
from p2CL_3CL import p2CL_3CL

# ax_CL_3CL = p2CL_3CL(fig, gspec[1:3, 1])

# 2nd Centre Right
from p2CR import p2CR

# ax_2CR = p2CR(fig, gspec[1, 2])

# 2nd Right
from p2R import p2R

# ax_2R = p2R(fig, gspec[1, 3])

# 3rd Left
from p3L import p3L

# ax_3L = p3L(fig, gspec[2, 0])

# 3rd Centre Right
from p3CR import p3CR

# ax_3CR = p3CR(fig, gspec[2, 2])

# 3rd and 4th Right
from p3R_4R import p3R_4R

# ax_3R_4R = p3R_4R(fig, gspec[2:4, 3], bg_im, bgi_extent)

# 4th and 5th Left
from p4L_5L import p4L_5L

# ax_4L_5L = p4L_5L(fig, gspec[3:5, 0])

# 4th Centre Left
from p4CL import p4CL

# ax_4CL = p4CL(fig, gspec[3, 1])

# 4th and 5th Centre Right
from p4CR_5CR import p4CR_5CR

# ax_4CR_5CR = p4CR_5CR(fig, gspec[3:5, 2])

# 5th Centre Left
from p5CL import p5CL

# ax_5CL = p5CL(fig, gspec[4, 1])

# 5th Right
from p5R import p5R

# ax_5R = p5R(fig, gspec[4, 3])

# Render the new image
fig.savefig("reimagine.webp")
