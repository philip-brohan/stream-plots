#!/usr/bin/env python

# Load 2 images and encode both into the SD latent space
# Merge the latent spaces into a new encoded image, and decode that image.
# Plot all three images, each with its latent space representation.

from PIL import Image
import numpy as np
from keras_cv.models import StableDiffusion

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle


model = StableDiffusion(img_width=1024, img_height=1024, jit_compile=True)


def load_image(path):
    im = Image.open(
        path,
        mode="r",
    )
    # Convert to numpy array on 0-1
    img = np.array(im) / 255.0
    # Add batch dimension
    img_batch = np.reshape(img, (1, 1024, 1024, 3))
    # Encode the image - into latent space
    latent = model.image_encoder.predict(img_batch)
    return (img, latent)


im1 = load_image("emoji.webp")
print(im1[0].shape)
print(im1[1].shape)
im2 = load_image("Ea-nāṣir.webp")
print(im2[0].shape)
print(im2[1].shape)

# Combine the latent spaces
lsc = im1[1]
lsc[:, :, :, 3] = im2[1][:, :, :, 3]

# Decode the combined latent space back into an image
recon = model.decoder.predict(lsc)

# Remove batch dimension
recon_img = np.reshape(recon, (1024, 1024, 3))

# Truncate to 0-1
recon_img = np.clip(recon_img, 0.0, 1.0)

# Figure showing the three images, each with their latent space
fig = Figure(
    figsize=((2 + 6) * 3, 6),  # Width, Height (inches)
    dpi=300,
    facecolor=(0.88, 0.88, 0.88, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=False,
    subplotpars=None,
    tight_layout=None,
)
canvas = FigureCanvas(fig)
font = {"family": "sans-serif", "sans-serif": "Arial", "weight": "normal", "size": 14}
matplotlib.rc("font", **font)

# Hack to get a white background
axb = fig.add_axes([0, 0, 1, 1])
axb.set_axis_off()
axb.add_patch(
    Rectangle(
        (0, 0),
        1,
        1,
        facecolor=(0.8, 0.8, 0.8, 1),
        fill=True,
        zorder=1,
    )
)


subfigs = fig.subfigures(
    nrows=1,
    ncols=6,
    wspace=0.01,
    hspace=0.01,
    width_ratios=[6, 1, 6, 1, 6, 1],
)


def fig_plot(sf1, sf2, img, latent):
    ax = sf1.subplots()
    ax.imshow(img)
    ax.axis("off")
    sf1.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

    ax = sf2.subplots(nrows=4, ncols=1, squeeze=False)
    for row in range(4):
        for col in range(1):
            ax[row, col].set_axis_off()
    ax[0, 0].imshow(latent[0, :, :, 0])
    ax[1, 0].imshow(latent[0, :, :, 1])
    ax[2, 0].imshow(latent[0, :, :, 2])
    ax[3, 0].imshow(latent[0, :, :, 3])


# Plot the images and their latent spaces
fig_plot(subfigs[0], subfigs[1], im1[0], im1[1])
fig_plot(subfigs[2], subfigs[3], im2[0], im2[1])
fig_plot(subfigs[4], subfigs[5], recon_img, lsc)


fig.savefig("ls_combine.webp")
