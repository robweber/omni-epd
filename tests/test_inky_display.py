import unittest
import pytest
import os
import sys
new_var = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
print(new_var)
sys.path.insert(0, new_var)

from omni_epd import displayfactory
from PIL import Image

image_path = os.path.dirname(os.path.realpath(__file__)) + '/../examples/PIA03519_small.jpg'


class TestInkyDisplay(unittest.TestCase):

    @pytest.mark.skip(reason="requires a connected inky")
    def test_auto_inky_with_color_display(self):
        epd = displayfactory.load_display_driver('inky.auto', {'EPD': {'mode': 'color'}})
        image = Image.open(image_path)
        image = image.resize((epd.width, epd.height))
        epd.display(image)