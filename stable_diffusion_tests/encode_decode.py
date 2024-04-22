#!/usr/bin/env python

# Load an image, and run it through the SD encoder and decoder

from PIL import Image
import numpy as np
from keras_cv.models import StableDiffusion

model = StableDiffusion(img_width=1024, img_height=1024, jit_compile=True)

# Load a sample image
# im = Image.open(r"Ea-nāṣir.webp")
im = Image.open(r"emoji.webp")

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

# Save the reconstructed image as a WebP
recon_im = Image.fromarray(np.uint8(recon_img * 255))
recon_im.save("recon.webp")
