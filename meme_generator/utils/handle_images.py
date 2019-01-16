import os
from PIL import Image


class HandleImage(object):
    """Create a Pillow object that resizes an image to a square aspect ratio"""

    def __init__(self, path, resize_size=1080):
        self.path = path
        self.original = Image.open(path)
        self.original_x = self.original.size[0]
        self.original_y = self.original.size[1]
        self.smallest_axis = self.calculate_smallest_axis(
            x=self.original_x, y=self.original_y)
        self.resize_size = resize_size
        self.scale = self.calculate_scale()
        self.resized = self.resize()
        self.resized_x = self.resized.size[0]
        self.resized_y = self.resized.size[1]
        self.crop_pixels = self.calculate_crop()
        self.crop_image = self.crop()

    def calculate_smallest_axis(self, x, y):
        """Calculate the smallest axis for further resizing and return string 'X' or 'Y'"""
        return "X" if x < y else "Y"

    def calculate_scale(self):
        """Calculate the scale ratio by dividing the smallest axis by resize size"""
        scale_divisor = self.original_x if self.smallest_axis == "X" else self.original_y
        return float(self.resize_size) / scale_divisor

    def resize(self):
        """Resize the image by the scaling amount"""
        dimensions = int(self.original_x *
                         self.scale), int(self.original_y * self.scale)
        return self.original.resize(dimensions)

    def calculate_crop(self):
        """Calculate how many pixels need to be removed from longer axis"""
        oversize = self.resized_x - \
            self.resized_y if self.smallest_axis == "Y" else self.resized_y - self.resized_x
        return oversize / 2

    def crop_x_smallest_axis(self):
        """Calculate cartesian coordinates if X is the smallest axis"""
        left = 0
        upper = self.crop_pixels
        right = self.resized_x
        lower = self.resized_y - self.crop_pixels
        return (left, upper, right, lower)

    def crop_y_smallest_axis(self):
        """Calculate cartesian coordinates if Y is the shortest axis"""
        left = self.crop_pixels
        upper = 0
        right = self.resized_x - self.crop_pixels
        lower = self.resized_y
        return (left, upper, right, lower)

    def crop(self):
        """Crop the excess pixels from the resized image"""
        box_coords = self.crop_x_smallest_axis(
        ) if self.smallest_axis == "X" else self.crop_y_smallest_axis()
        crop = self.resized.crop(box_coords)

        check_x = crop.size[0]
        check_y = crop.size[1]

        if check_x > 1080 or check_y > 1080:
            crop = crop.crop((0, 0, 1080, 1080))

        return crop

    def get_cropped(self):
        """Return the Pillow image object of the cropped image"""
        return self.crop_image

    def save(self, path):
        """Save the cropped image to the supplied path"""
        self.crop_image.save(path)
