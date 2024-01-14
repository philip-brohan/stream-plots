#!/usr/bin/env python

# Test run of stable diffusion (slow on CPU)

import PIL.Image
import keras_cv

# Load Stable Diffusion model
model = keras_cv.models.StableDiffusion(
    img_width=512, img_height=512, jit_compile=False
)
images = model.text_to_image(
    "A scientist in an early 20th-century style laboratory, with weather maps",
    # + " surrounded by weather maps and calculation tools, reminiscent"
    # + " of L. F. Richardson's work in meteorology and mathematical physics."
    # + " The scientist, a Caucasian male with a thoughtful expression,"
    # + " is examining a complex weather map on a large table, with various"
    # + " mathematical instruments scattered around. The room is filled with old books,"
    # + " charts, and a blackboard with equations, reflecting the era's scientific ambiance.",
    batch_size=3,
)

for i in range(images.shape[0]):
    img = PIL.Image.fromarray(images[i, :, :, :])
    img.save("sd.png")
