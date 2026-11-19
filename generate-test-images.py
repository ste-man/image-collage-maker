#!/usr/bin/env python3
"""Generate 100 PNG images with random dimensions.

What the script does:
  1. Creates a folder named "generated-images" in the current working
     directory (the folder you are in when you run the script). If the
     folder already exists, it is reused.
  2. Generates 100 images. Each image gets a random width and a random
     height, both between 1000 and 2000 pixels (inclusive).
  3. Saves each image into the "generated-images" folder using the name
         image-[xxx]_[x-size]-[y-size].png
     where [xxx] is a zero-padded sequence number starting at 001,
     e.g. image-001_1534-1187.png.

Requirements:
  Pillow (the Python imaging library):  pip install Pillow

Usage:
  python3 generate_images.py
"""

# --- Imports ---------------------------------------------------------------
# random  : picks the random image sizes and background colours.
# pathlib : builds file and folder paths that work on any operating system.
# PIL     : Pillow, which creates the images, draws on them and saves them.
import random
from pathlib import Path

from PIL import Image, ImageDraw

# --- Settings --------------------------------------------------------------
# Change these values to adjust how many images are made and how large they
# can be. MIN_SIZE and MAX_SIZE apply to both the width and the height.
NUM_IMAGES = 100       # total number of images to generate
MIN_SIZE = 1000        # smallest allowed width/height in pixels
MAX_SIZE = 2000        # largest allowed width/height in pixels
OUTPUT_DIR_NAME = "generated-images"  # folder created in the current directory


def make_image(width: int, height: int, label: str) -> Image.Image:
    """Create one image of the given size with a coloured background and a label.

    Args:
        width:  image width in pixels.
        height: image height in pixels.
        label:  text drawn in the centre of the image.

    Returns:
        A Pillow Image object (held in memory, not yet saved to disk).
    """
    # Pick a random background colour as an (R, G, B) tuple. Each channel is
    # a whole number from 0 to 255.
    bg = tuple(random.randint(0, 255) for _ in range(3))

    # Create a new RGB image of the requested size, filled with that colour.
    img = Image.new("RGB", (width, height), bg)

    # Work out how bright the background is, using the standard formula for
    # perceived brightness (green looks brightest to the eye, blue darkest).
    # The result is between 0 (black) and 255 (white).
    luminance = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]

    # Use black text on light backgrounds and white text on dark ones so the
    # label is always easy to read.
    fg = (0, 0, 0) if luminance > 128 else (255, 255, 255)

    # ImageDraw lets us draw shapes and text onto the image.
    draw = ImageDraw.Draw(img)

    # Draw the label in the centre of the image:
    #   - (width / 2, height / 2) is the centre point.
    #   - anchor="mm" means "middle-middle": the text is centred on that point
    #     both horizontally and vertically.
    #   - font_size scales with the image (1/20 of its longest side) so the
    #     text looks a similar size on every image.
    draw.text(
        (width / 2, height / 2),
        label,
        fill=fg,
        anchor="mm",
        font_size=max(width, height) // 20,
    )
    return img


def main() -> None:
    """Create the output folder, then generate and save all the images."""
    # Path.cwd() is the current working directory, i.e. the folder the
    # script is run from (not necessarily the folder the script is stored in).
    out_dir = Path.cwd() / OUTPUT_DIR_NAME

    # Create the folder. exist_ok=True means no error is raised if the folder
    # is already there; existing files with the same names are overwritten.
    out_dir.mkdir(exist_ok=True)

    # Loop from 1 to NUM_IMAGES (inclusive); i is the image's sequence number.
    for i in range(1, NUM_IMAGES + 1):
        # Choose a random width and height. randint includes both end points,
        # so 1000 and 2000 are both possible values.
        width = random.randint(MIN_SIZE, MAX_SIZE)
        height = random.randint(MIN_SIZE, MAX_SIZE)

        # Build the file name. {i:03d} formats the number as at least three
        # digits, padding with leading zeros: 1 -> "001", 42 -> "042".
        filename = f"image-{i:03d}_{width}-{height}.png"

        # Create the image, labelled with its number and size so each one is
        # easy to identify when opened.
        img = make_image(width, height, f"{i:03d}  {width}x{height}")

        # Save it as a PNG in the output folder. Pillow chooses the PNG format
        # from the ".png" file extension.
        img.save(out_dir / filename)
        print(f"Saved {filename}")

    # Print a summary showing exactly where the images were written.
    print(f"\nDone: {NUM_IMAGES} images written to {out_dir}")


# Run main() only when the file is executed directly
# (e.g. "python3 generate_images.py"), not when it is imported by another script.
if __name__ == "__main__":
    main()
