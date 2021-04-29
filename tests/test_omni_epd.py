import unittest
import os
import time
import json
from omni_epd import EPDNotFoundError, EPDConfigurationError
from omni_epd import displayfactory
from omni_epd.virtualepd import VirtualEPD
from omni_epd.conf import IMAGE_DISPLAY, CONFIG_FILE


class TestomniEpd(unittest.TestCase):
    goodEpd = "omni_epd.mock"  # this should always be a valid EPD
    badEpd = "omni_epd.bad"  # this is not a valid EPD
    badConfig = 'bad_conf.ini'  # name of invalid configuration file

    def test_supported_diplays(self):
        """
        Test that displays can be loaded
        """
        drivers = displayfactory.list_supported_displays()

        assert len(drivers) > 0

    def test_loading_error(self):
        """
        Confirm error thrown if an invalid name passed to load function
        """
        self.assertRaises(EPDNotFoundError, displayfactory.load_display_driver, self.badEpd)

    def test_loading_success(self):
        """
        Confirm a good display can be loaded and extends VirtualEPD
        """
        epd = displayfactory.load_display_driver(self.goodEpd)

        assert isinstance(epd, VirtualEPD)

    def test_global_conf(self):
        """
        Test loading of omni-epd.ini config file
        Once loaded confirm options from file exist within display class config
        Also confirm values not in the config file aren't changed from defaults
        """
        # set up a global config file
        os.rename(os.path.join(os.getcwd(), "tests", CONFIG_FILE), os.path.join(os.getcwd(), CONFIG_FILE))
        time.sleep(1)

        epd = displayfactory.load_display_driver(self.goodEpd)

        assert epd._config.has_option(IMAGE_DISPLAY, 'rotate')
        assert epd._config.getfloat(IMAGE_DISPLAY, 'rotate') == 90

        # test that mode is default
        assert epd.mode == 'bw'

        # reset global config file, wait for file IO
        os.rename(os.path.join(os.getcwd(), CONFIG_FILE), os.path.join(os.getcwd(), "tests", CONFIG_FILE))
        time.sleep(1)

    def test_device_config(self):
        """
        Test that when both omni-epd.ini file is present and device specific INI present
        that the device specific config overrides options in global config
        """
        deviceConfig = self.goodEpd + ".ini"

        # set up a global config file and device config
        os.rename(os.path.join(os.getcwd(), "tests", CONFIG_FILE), os.path.join(os.getcwd(), CONFIG_FILE))
        os.rename(os.path.join(os.getcwd(), "tests", deviceConfig), os.path.join(os.getcwd(), deviceConfig))
        time.sleep(1)

        epd = displayfactory.load_display_driver(self.goodEpd)

        # device should override global
        assert epd._config.has_option(IMAGE_DISPLAY, 'flip_horizontal')
        self.assertFalse(epd._config.getboolean(IMAGE_DISPLAY, 'flip_horizontal'))

        # test mode and palette configurations
        assert epd.mode == 'palette'
        assert len(json.loads(epd._get_device_option('palette_filter', "[]"))) == 5  # confirms custom palette will be loaded

        # reset global config file, wait for file IO
        os.rename(os.path.join(os.getcwd(), CONFIG_FILE), os.path.join(os.getcwd(), "tests", CONFIG_FILE))
        os.rename(os.path.join(os.getcwd(), deviceConfig), os.path.join(os.getcwd(), "tests", deviceConfig))
        time.sleep(1)

    def test_load_device_from_conf(self):
        """
        Test that a device will load when given the type= option in the omni-epd.ini file
        and no args to load_display_driver()
        """
        deviceConfig = self.goodEpd + ".ini"

        # set up a global config file
        os.rename(os.path.join(os.getcwd(), "tests", CONFIG_FILE), os.path.join(os.getcwd(), CONFIG_FILE))
        os.rename(os.path.join(os.getcwd(), "tests", deviceConfig), os.path.join(os.getcwd(), deviceConfig))
        time.sleep(1)

        # should load driver from ini file without error
        epd = displayfactory.load_display_driver()

        # test that driver specific file also loaded
        assert epd._config.has_option(IMAGE_DISPLAY, 'flip_horizontal')
        self.assertFalse(epd._config.getboolean(IMAGE_DISPLAY, 'flip_horizontal'))

        # should attempt to load passed in driver, and fail, instead of one in conf file
        self.assertRaises(EPDNotFoundError, displayfactory.load_display_driver, self.badEpd)

        # reset global config file, wait for file IO
        os.rename(os.path.join(os.getcwd(), CONFIG_FILE), os.path.join(os.getcwd(), "tests", CONFIG_FILE))
        os.rename(os.path.join(os.getcwd(), deviceConfig), os.path.join(os.getcwd(), "tests", deviceConfig))
        time.sleep(1)

    def test_configuration_error(self):
        """
        Confirm that an EPDConfigurationError is thrown by passing a bad mode value
        to a display
        """
        deviceConfig = self.goodEpd + ".ini"

        # copy bad config file to be loaded
        os.rename(os.path.join(os.getcwd(), "tests", self.badConfig), os.path.join(os.getcwd(), deviceConfig))

        # load the display driver, shoudl throw EPDConfigurationError
        self.assertRaises(EPDConfigurationError, displayfactory.load_display_driver, self.goodEpd)

        os.rename(os.path.join(os.getcwd(), deviceConfig), os.path.join(os.getcwd(), "tests", self.badConfig))
        time.sleep(1)
