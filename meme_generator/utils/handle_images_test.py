import os
import pytest
from PIL import Image

from handle_images import HandleImage


def create_image(w, h):
    living_coral = 250, 114, 104  # Pantone colour of the year 2019, obv
    return Image.new("RGB", (w, h), living_coral)


class TestResizedSizes(object):
    def test_create_image(self):
        test_image = create_image(50, 50)
        assert test_image.size == (50, 50)
        test_image.close()

    def test_640_360_is_cropped_1080_square(self):
        sixteen_nine = os.path.abspath("sixteen_nine.jpg")
        create_image(640, 360).save(sixteen_nine)
        cropped = HandleImage(sixteen_nine).get_cropped()
        assert cropped.size == (1080, 1080)
        cropped.close()
        os.remove(sixteen_nine)

    def test_845_267_is_cropped_1080_square(self):
        random_ar = os.path.abspath("random_ar.jpg")
        create_image(845, 267).save(random_ar)
        cropped = HandleImage(random_ar).get_cropped()
        assert cropped.size == (1080, 1080)
        cropped.close()
        os.remove(random_ar)

    def test_1920_1080_is_cropped_1080_square(self):
        sixteen_oversized = os.path.abspath("sixteen_oversized.jpg")
        create_image(1920, 1080).save(sixteen_oversized)
        cropped = HandleImage(sixteen_oversized).get_cropped()
        assert cropped.size == (1080, 1080)
        cropped.close()
        os.remove(sixteen_oversized)

    def test_360_640_is_cropped_1080_square(self):
        nine_sixteen = os.path.abspath("nine_sixteen.jpg")
        create_image(640, 360).save(nine_sixteen)
        cropped = HandleImage(nine_sixteen).get_cropped()
        assert cropped.size == (1080, 1080)
        cropped.close()
        os.remove(nine_sixteen)

    def test_347_941_is_cropped_1080_square(self):
        random_ar = os.path.abspath("random_ar.jpg")
        create_image(845, 267).save(random_ar)
        cropped = HandleImage(random_ar).get_cropped()
        assert cropped.size == (1080, 1080)
        cropped.close()
        os.remove(random_ar)

    def test_1080_1920_is_cropped_1080_square(self):
        nine_oversized = os.path.abspath("nine_oversized.jpg")
        create_image(1920, 1080).save(nine_oversized)
        cropped = HandleImage(nine_oversized).get_cropped()
        assert cropped.size == (1080, 1080)
        cropped.close()
        os.remove(nine_oversized)
