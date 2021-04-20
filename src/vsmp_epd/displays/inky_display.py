"""
Copyright 2021 Rob Weber

This file is part of vsmp-epd

vsmp-epd is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from .. conf import IMAGE_ENHANCEMENTS
from .. virtualepd import VirtualEPD


class InkyDisplay(VirtualEPD):
    """
    This is an abstraction for Pimoroni Inky pHat and wHat devices
    https://github.com/pimoroni/inky
    """

    pkg_name = 'inky'

    def __init__(self, deviceName, config):
        super(InkyDisplay, self).__init__(deviceName, config)

        # if color does not exist, add it
        if(not self._config.has_option(IMAGE_ENHANCEMENTS, "color")):
            if(not self._config.has_section(IMAGE_ENHANCEMENTS)):
                self._config.add_section(IMAGE_ENHANCEMENTS)

            # by default use black/white images
            self._config.set(IMAGE_ENHANCEMENTS, "color", "1")

        # need to figure out what type of device we have
        dType, dColor = deviceName.split('_')

        if(dType == 'phat'):
            deviceObj = self.load_display_driver(self.pkg_name, 'phat')
            self._device = deviceObj.InkyPHAT(dColor)
        elif(dType == 'phat1608'):
            deviceObj = self.load_display_driver(self.pkg_name, 'phat')
            self._device = deviceObj.InkyPHAT_SSD1608(dColor)
        elif(dType == 'what'):
            deviceObj = self.load_display_driver(self.pkg_name, 'what')
            self._device = deviceObj.InkyWHAT(dColor)

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        result = []

        deviceList = ["phat_black", "phat_red", "phat_yellow",
                      "phat1608_black", "phat1608_red", "phat1608_yellow"
                      "what_black", "what_red", "what_yellow"]

        try:
            # do a test import from the inky library
            from inky import WHITE  # noqa: F401

            # if passed return list of devices
            result = [f"{InkyDisplay.pkg_name}.{n}" for n in deviceList]
        except ModuleNotFoundError:
            # python libs for this might not be installed - that's ok, return nothing
            pass

        return result

    def _display(self, image):
        self._device.set_image(image)
        self._device.show()

    def clear(self):
        from inky import WHITE

        for _ in range(2):
            for y in range(self.height - 1):
                for x in range(self.width - 1):
                    self._device.set_pixel(x, y, WHITE)

        self._device.show()


class InkyImpressionDisplay(VirtualEPD):
    """
    This is an abstraction for Pimoroni Inky Impression devices
    https://shop.pimoroni.com/products/inky-impression
    https://github.com/pimoroni/inky
    """

    pkg_name = 'inky'

    def __init__(self, deviceName, config):
        super(InkyDisplay, self).__init__(deviceName, config)

        # load the device driver
        deviceObj = self.load_display_driver(self.pkg_name, 'inky_uc8159')
        self._device = deviceObj.Inky()

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        result = []

        try:
            # do a test import from the inky library
            from inky.inky_uc8159 import CLEAN  # noqa: F401

            # if passed return list of devices
            result = [f"{InkyDisplay.pkg_name}.impression"]
        except ModuleNotFoundError:
            # python libs for this might not be installed - that's ok, return nothing
            pass

        return result

    def _display(self, image):
        self._device.set_image(image)
        self._device.show()

    def clear(self):
        from inky.inky_uc8159 import CLEAN

        for _ in range(2):
            for y in range(self.height - 1):
                for x in range(self.width - 1):
                    self._device.set_pixel(x, y, CLEAN)

        self._device.show()
