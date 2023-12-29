#!/usr/bin/env python

# Test run of stable diffusion (slow on CPU)

import PIL.Image
import keras_cv

# Load Stable Diffusion model
model = keras_cv.models.StableDiffusion(
    img_width=512, img_height=512, jit_compile=False
)
images = model.text_to_image("photograph of an astronaut riding a horse", batch_size=1)

img = PIL.Image.fromarray(images[0, :, :, :])
img.save("sd.png")
