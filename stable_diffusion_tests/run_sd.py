#!/usr/bin/env python

# Test run of stable diffusion (slow on CPU)

import PIL.Image
import keras
from keras import ops
import keras_cv

# Load Stable Diffusion model
model = keras_cv.models.StableDiffusion(
    jit_compile=False,
)

# Encode a text prompt into latent space
latent = ops.squeeze(
    model.encode_text(
        "A scientist in an early 20th-century style laboratory, with weather maps"
    )
)

# Show the size of the latent manifold
print(f"Encoding shape: {latent.shape}")

# Make the diffusion noise
seed = 12345
noise = keras.random.normal((512 // 8, 512 // 8, 4), seed=seed)

images = model.generate_image(
    latent,
    batch_size=1,
    diffusion_noise=noise,
)

for i in range(images.shape[0]):
    img = PIL.Image.fromarray(images[i, :, :, :])
    img.save("sd.webp", "webp", lossless=True)
