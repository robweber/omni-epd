
from omni_epd import displayfactory
from PIL import Image
import unittest
import pytest
import os

image_path = os.path.dirname(os.path.realpath(__file__)) + '/../examples/PIA03519_small.jpg'


class TestInkyDisplay(unittest.TestCase):

    @pytest.mark.skip(reason="requires a connected inky")
    def test_auto_inky_with_color_display(self):
        epd = displayfactory.load_display_driver('inky.impression', {'EPD': {'mode': 'color'}})
        image = Image.open(image_path)
        image = image.resize((epd.width, epd.height))
        epd.display(image)
        epd.close()