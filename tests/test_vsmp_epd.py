import unittest
from vsmp_epd import displayfactory
from vsmp_epd.virtualepd import VirtualEPD


class TestVsmpEpd(unittest.TestCase):
    goodEpd = "vsmp_epd.mock"  # this should always be a valid EPD
    badEpd = "vsmp_epd.bad"  # this is not a valid EPD

    def test_supported_diplays(self):
        drivers = displayfactory.list_supported_displays()

        assert len(drivers) > 0

    def test_loading_error(self):
        self.assertRaises(displayfactory.EPDNotFoundError, displayfactory.load_display_driver, self.badEpd)

    def test_loading_success(self):
        epd = displayfactory.load_display_driver(self.goodEpd)

        assert isinstance(epd, VirtualEPD)
