from PIL import Image
from pathlib import Path


def add_watermark(input_path, watermark_path, output_path):
    """Add EU-compliant meme watermark to a supplied image"""
    try:
        original_image = Image.open(input_path)
        _w, h = original_image.size
        size = int(round(h * 0.4))
        watermark_image = Image.open(watermark_path)
        watermark_image.thumbnail((size, size))
        print(watermark_image.size)
        _resized_width, resized_height = watermark_image.size

        original_image.paste(watermark_image, (8, h - resized_height - 8),
                             mask=watermark_image)
        original_image.save(output_path)
        return "Success!"
    except IOError:
        return "Failure!"
