#!/usr/bin/env python

# Random emoji image at 1024x1024 pixels

import os
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import random

# Emoji font to use
pad = 10  # Padding between emoji
fontsize = 109  # Fixed
font = ImageFont.truetype(
    r"%s/fonts/NotoColorEmoji.ttf" % os.getenv("CONDA_PREFIX"), fontsize
)
# Get a list of all the code points in the font
font2 = TTFont(r"%s/fonts/NotoColorEmoji.ttf" % os.getenv("CONDA_PREFIX"))
# Get the 'cmap' table, which maps character codes to glyph names
cmap = font2.getBestCmap()
# The keys of the 'cmap' table are the supported Unicode code points
supported_code_points = list(cmap.keys())

# Image to draw on
plot_width = 1024
plot_height = 1024
bgcol = (225, 225, 225)
img = Image.new(
    mode="RGB",
    size=(1024, 1024),
    color=bgcol,
)
draw = ImageDraw.Draw(img)

# Draw random emoji
nxChar = int(plot_width / (fontsize + pad)) + 1
nyChar = int(plot_height / (fontsize + pad)) + 1
for h in range(nxChar):
    for w in range(nyChar):
        pChar = chr(random.choice(supported_code_points))
        draw.text(
            (w * (fontsize + pad) + pad / 2, h * (fontsize + pad) + pad / 2),
            pChar,
            font=font,
            embedded_color=True,
        )
        pChar = chr(random.choice(supported_code_points))
        draw.text(
            (
                (w + 0.5) * (fontsize + pad) + pad / 2,
                (h + 0.5) * (fontsize + pad) + pad / 2,
            ),
            pChar,
            font=font,
            embedded_color=True,
        )

img.save("emoji.webp", "webp", lossless=True)
