#!/usr/bin/env python

# Re-draw Durer's Rhinecerous using Matplotlib

import sys
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Polygon

from PIL import Image
import numpy as np
from scipy.interpolate import make_interp_spline

# Load the original
im = Image.open(r"The_Rhinoceros_(NGA_1964.8.697)_enhanced.png")
im = im.convert("RGB")
# Convert to numpy array on 0-1
im = np.array(im) / 255.0

# Figure showing the original image, reconstructed image, and latent space
bgcolor = (242 / 255, 231 / 255, 218 / 255, 1)
fig = Figure(
    figsize=(3000 / 100, 2368 / 100),  # Width, Height (inches)
    dpi=300,
    facecolor=bgcolor,
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


# Utility fn to make a smooth line from segments
def smoothLine(pts, n=100):
    spline = make_interp_spline(pts[:, 0], pts[:, 1], k=3)
    x = np.linspace(pts[:, 0].min(), pts[:, 0].max(), n)
    y = spline(x)
    return np.stack([x, y], axis=1)


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
# Polygon points matched to original
poly_TL = smoothLine(
    np.array([[30, -0.1], [35, 0], [50, 0.3], [100, 0.65], [110, 0.7]])
)
# Close the polygon by inserting elements outside of the axes window
poly_TL = np.append(poly_TL, [[110, 0.1]], axis=0)
ax_TL.fill_between(
    poly_TL[:, 0], poly_TL[:, 1], color="none", edgecolor="black", hatch="//"
)

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

# Line points matched to original
line_TCL = smoothLine(
    np.array(
        [
            [0, 0.72],
            [5, 0.82],
            [10, 0.72],
            [20, 0.68],
            [30, 0.65],
            [40, 0.63],
            [50, 0.6],
            [75, 0.63],
            [100, 0.65],
        ]
    )
)
ax_TCL.plot(line_TCL[:, 0], line_TCL[:, 1], color="red", linewidth=5, marker="none")

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
xy = np.array(
    [
        [5, 0.65],
        [3, 0.58],
        [4, 0.49],
        [5, 0.4],
        [2, 0.05],
        [5, 0.15],
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
    ]
)
colors = matplotlib.colormaps["viridis"](np.random.rand(len(xy)))
size = 1000
ax_23CL.scatter(xy[:, 0], xy[:, 1], c=colors, s=size, alpha=0.5)
ax_23CL.scatter(xy[:, 0], xy[:, 1], c="white", s=size / 4, alpha=0.5)

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
    cmap="viridis",
    edgecolors="white",
    alpha=0.5,
    zorder=100,
)
# Polygon points matched to original
poly_3L = np.array([[73, 1.1], [75, 1], [80, 0.7], [90, 0.3], [100, 0.1], [110, 0.1]])
# Smooth the polygon
spline = make_interp_spline(poly_3L[:, 0], poly_3L[:, 1], k=3)
x = np.linspace(poly_3L[:, 0].min(), poly_3L[:, 0].max(), 100)
y = spline(x)
# Draw the line to be a shadow effect
ax_3L.plot(
    poly_3L[:, 0] - 1,
    poly_3L[:, 1] - 0.01,
    color=(0, 0, 0, 0.2),
    linewidth=3,
    marker="none",
    zorder=200,
)
# Close the polygon by inserting elements outside of the axes window
x = np.append(x, [110, 73])
y = np.append(y, [1.1, 1.1])
poly_3L = np.stack([x, y], axis=1)
ax_3L.fill_between(
    poly_3L[:, 0],
    poly_3L[:, 1],
    color=bgcolor,
    edgecolor="none",
    zorder=300,
)
x = [80, 85, 90, 95, 93, 97, 95, 92]
y = [0.95, 0.7, 0.4, 0.25, 0.8, 0.49, 0.9, 0.6]
xe = [4, 5, 3, 3, 6, 2, 2, 2]
ye = [0.15, 0.14, 0.1, 0.08, 0.05, 0.15, 0.05, 0.05]
color = matplotlib.colormaps["viridis"](np.random.rand(len(x)))
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
# Ground shading with a clipped gradient
phi = 0.5 * np.pi / 2
v = np.array([np.cos(phi), np.sin(phi)])
X = np.array([[v @ [1, 0], v @ [1, 1]], [v @ [0, 0], v @ [0, 1]]])
a, b = (0, 1)
X = a + (b - a) / X.max() * X
im = ax_45L.imshow(
    X,
    interpolation="bicubic",
    clim=(0, 1),
    aspect="auto",
    extent=(100, 0, 0, 1),
    cmap="Reds",
    alpha=0.5,
)
im.set_clip_path(
    Polygon([[0, 0], [0, 0.4], [100, 0.6], [100, 0]], transform=ax_45L.transData)
)


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
# Use a grid to imitate the shading shadow
ax_5CL.set_yticks(np.linspace(0.2, 0.9, 25), minor=True)
ax_5CL.grid(
    visible=True, which="minor", axis="y", color="black", linestyle="-", linewidth=0.5
)

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
# Add a bar chart
ax_5R.bar(
    [10, 30, 50, 70, 90],
    [0.9, 0.8, 0.75, 0.7, 0.75],
    width=18,
    color="none",
    edgecolor="black",
    hatch="x",
)

# Render the new image
fig.savefig("reimagine.webp")
