
from omni_epd import displayfactory
from PIL import Image
import unittest
import pytest
import os
import time

image_path = os.path.dirname(os.path.realpath(__file__)) + '/../examples/PIA03519_small.jpg'

inky_impression = 'inky.impression'
inky_auto = 'inky.auto'
waveshare_27bV2 = 'waveshare_epd.epd2in7b_V2'
waveshare_42bV2 = 'waveshare_epd.epd4in2b_V2'

empty_config = {}
color_config = {'EPD': {'mode': 'color'}}
red_config = {'EPD': {'mode': 'red'}}

test_params = [
    ('impression in color mode', inky_impression, color_config),
    ('impression in default mode', inky_impression, empty_config),
    ('auto in color mode', inky_auto, color_config),
    ('auto in default mode', inky_auto, empty_config),
    ('epd2in7b_V2 in red mode', waveshare_27bV2, red_config),
    ('epd2in7b_V2 in default mode', waveshare_27bV2, empty_config),
    ('epd4in2b_V2 in red mode', waveshare_42bV2, red_config),
    ('epd4in2b_V2 in default mode', waveshare_42bV2, empty_config),
]


class DeviceMetaTest(type):
    def __new__(mcs, name, bases, dict):
        def gen_test(name, device, config_dict):
            def test(self):
                epd = displayfactory.load_display_driver(device, config_dict)
                epd.prepare()
                # display image
                epd.display(Image.open(image_path).resize((epd.width, epd.height)))
                # wait while you verify the image
                #time.sleep(5)
                # clear the image after
                #epd.clear()
                epd.close()
            return test

        for test_param in test_params:
            test_name = "test %s" % test_param[0]
            dict[test_name] = gen_test(*test_param)

        return type.__new__(mcs, name, bases, dict)


@pytest.mark.skip("requires a connected epd")
class TestInkyDeviceWithConfigs(unittest.TestCase, metaclass=DeviceMetaTest):
    __metaclass__ = DeviceMetaTest
