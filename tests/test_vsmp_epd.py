import unittest
import os
import time
from vsmp_epd import EPDNotFoundError
from vsmp_epd import displayfactory
from vsmp_epd.virtualepd import VirtualEPD
from vsmp_epd.conf import IMAGE_DISPLAY, CONFIG_FILE

class TestVsmpEpd(unittest.TestCase):
    goodEpd = "vsmp_epd.mock"  # this should always be a valid EPD
    badEpd = "vsmp_epd.bad"  # this is not a valid EPD

    def test_supported_diplays(self):
        drivers = displayfactory.list_supported_displays()

        assert len(drivers) > 0

    def test_loading_error(self):
        self.assertRaises(EPDNotFoundError, displayfactory.load_display_driver, self.badEpd)

    def test_loading_success(self):
        epd = displayfactory.load_display_driver(self.goodEpd)

        assert isinstance(epd, VirtualEPD)

    def test_global_conf(self):
        # set up a global config file
        os.rename(os.path.join(os.getcwd(), "tests", CONFIG_FILE), os.path.join(os.getcwd(), CONFIG_FILE))
        time.sleep(1)

        epd = displayfactory.load_display_driver(self.goodEpd)

        assert epd._config.has_option(IMAGE_DISPLAY, 'rotate') == True
        assert epd._config.getfloat(IMAGE_DISPLAY, 'rotate') == 90

        # reset global config file, wait for file IO
        os.rename(os.path.join(os.getcwd(), CONFIG_FILE), os.path.join(os.getcwd(), "tests", CONFIG_FILE))
        time.sleep(1)

    def test_device_config(self):
        deviceConfig = self.goodEpd + ".ini"

        # set up a global config file and device config
        os.rename(os.path.join(os.getcwd(), "tests", CONFIG_FILE), os.path.join(os.getcwd(), CONFIG_FILE))
        os.rename(os.path.join(os.getcwd(), "tests", deviceConfig), os.path.join(os.getcwd(), deviceConfig))
        time.sleep(1)

        epd = displayfactory.load_display_driver(self.goodEpd)

        # device should override global
        assert epd._config.has_option(IMAGE_DISPLAY, 'flip_horizontal') == True
        assert epd._config.getboolean(IMAGE_DISPLAY, 'flip_horizontal') == False

        # reset global config file, wait for file IO
        os.rename(os.path.join(os.getcwd(), CONFIG_FILE), os.path.join(os.getcwd(), "tests", CONFIG_FILE))
        os.rename(os.path.join(os.getcwd(), deviceConfig), os.path.join(os.getcwd(), "tests", deviceConfig))
        time.sleep(1)
