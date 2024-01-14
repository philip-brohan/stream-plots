#!/usr/bin/env python

# Load an image, and run it through the SD encoder and decoder
# Plot both images, and the latent space.

from PIL import Image
import numpy as np
from keras_cv.models import StableDiffusion

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle


model = StableDiffusion(img_width=1024, img_height=1024, jit_compile=True)

# Load a sample image
im = Image.open(r"Ea-nāṣir.webp")

# Convert to numpy array on 0-1
img = np.array(im) / 255.0

# Add batch dimension
img_batch = np.reshape(img, (1, 1024, 1024, 3))

# Encode the image - into latent space
latent = model.image_encoder.predict(img_batch)

# Decode the latent space back into an image
recon = model.decoder.predict(latent)

# Remove batch dimension
recon_img = np.reshape(recon, (1024, 1024, 3))

# Truncate to 0-1
recon_img = np.clip(recon_img, 0.0, 1.0)

# Figure showing the original image, reconstructed image, and latent space
fig = Figure(
    figsize=(4 + 1 + 4, 4),  # Width, Height (inches)
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
    ncols=3,
    wspace=0.01,
    hspace=0.01,
    width_ratios=[6, 2, 6],
)

# Left hand subfig has original
ax = subfigs[0].subplots()
ax.imshow(img)
ax.axis("off")
subfigs[0].subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

# right hand subfig has reconstruction
ax = subfigs[2].subplots()
ax.imshow(recon_img)
ax.axis("off")

# Centre subfig has latent space
ax = subfigs[1].subplots(nrows=4, ncols=1, squeeze=False)
for row in range(4):
    for col in range(1):
        ax[row, col].set_axis_off()
ax[0, 0].imshow(latent[0, :, :, 0])
ax[1, 0].imshow(latent[0, :, :, 1])
ax[2, 0].imshow(latent[0, :, :, 2])
ax[3, 0].imshow(latent[0, :, :, 3])

fig.savefig("encode-decode.webp")
