#!/usr/bin/env python

# Load an image, and run it through the SD encoder and decoder

from PIL import Image
import numpy as np
from keras_cv.models import StableDiffusion

model = StableDiffusion(img_width=1024, img_height=1024, jit_compile=True)

# Load a sample image
im = Image.open(r"Ea-nāṣir.webp")
img = np.array(im)

img_batch = np.reshape(img, (1, 1024, 1024, 3))

latent = model.image_encoder.predict(img_batch)

recon = model.decoder.predict(latent)

recon_img = np.reshape(recon, (1024, 1024, 3))  # Remove batch dimension

# Save the reconstructed image  as a PNG
recon_im = Image.fromarray(np.uint8(recon_img * 255))
recon_im.save("recon.webp")
