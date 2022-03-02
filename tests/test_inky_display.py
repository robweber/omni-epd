
from omni_epd import displayfactory
from PIL import Image
import unittest
import pytest
import os


image_path = os.path.dirname(os.path.realpath(__file__)) + '/../examples/PIA03519_small.jpg'
inky_impression = 'inky.impression'
inky_auto = 'inky.auto'
empty_config = {}
color_config = {'EPD': {'mode': 'color'}}

test_params = [
    ('impression in color mode', inky_impression, color_config),
    ('impression in default mode', inky_impression, empty_config),
    ('auto in color mode', inky_auto, color_config),
    ('auto in default mode', inky_auto, empty_config),
]


class DeviceMetaTest(type):
    def __new__(mcs, name, bases, dict):
        def gen_test(name, device, config_dict):
            def test(self):
                epd = displayfactory.load_display_driver(device, config_dict)
                image = Image.open(image_path)
                image = image.resize((epd.width, epd.height))
                epd.display(image)
                epd.close()

            return test

        for test_param in test_params:
            test_name = "test %s" % test_param[0]
            dict[test_name] = gen_test(*test_param)

        return type.__new__(mcs, name, bases, dict)


@pytest.mark.skip("requires a connected inky")
class TestInkyDeviceWithConfigs(unittest.TestCase, metaclass=DeviceMetaTest):
    __metaclass__ = DeviceMetaTest
