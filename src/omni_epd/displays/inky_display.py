"""
Copyright 2021 Rob Weber

This file is part of omni-epd

omni-epd is free software: you can redistribute it and/or modify
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

from .. virtualepd import VirtualEPD


class InkyDisplay(VirtualEPD):
    """
    This is an abstraction for Pimoroni Inky pHat and wHat devices
    https://github.com/pimoroni/inky
    """

    pkg_name = 'inky'
    mode = "black"  # default mode is black
    _modes_available = ("black")

    def __init__(self, deviceName, config):
        super(InkyDisplay, self).__init__(deviceName, config)

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

        # could have additional display modes
        # phat and what devices expect colors in the order white, black, other
        if(dColor == 'red' and self.mode != 'black'):
            self._modes_available = ('black', 'red')
            self.palette_filter.append([255, 0, 0])
            self.max_colors = 3
        elif(dColor == 'yellow' and self.mode != 'bw'):
            self._modes_available = ('black', 'yellow')
            self.palette_filter.append([255, 255, 0])
            self.max_colors = 3

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        result = []

        deviceList = ["phat_black", "phat_red", "phat_yellow",
                      "phat1608_black", "phat1608_red", "phat1608_yellow",
                      "what_black", "what_red", "what_yellow"]

        # python libs for this might not be installed - that's ok, return nothing
        if(InkyDisplay.check_module_installed('inky')):
            # if passed return list of devices
            result = [f"{InkyDisplay.pkg_name}.{n}" for n in deviceList]

        return result

    def _display(self, image):
        # apply any needed conversions to this image based on the mode
        image = self._filterImage(image)

        # set the image and display
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
    mode = 'color'  # this uses color by default

    def __init__(self, deviceName, config):
        super(InkyDisplay, self).__init__(deviceName, config)

        # load the device driver
        deviceObj = self.load_display_driver(self.pkg_name, 'inky_uc8159')
        self._device = deviceObj.Inky()

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

        # get colors from the inky lib (won't be used normally as inky does conversion)
        self.palette_filter = self._device.DESATURATED_PALETTE
        self.max_colors = 8  # 7 + transparent
        self._modes_available = ('bw', 'color')

    @staticmethod
    def get_supported_devices():
        result = []

        # python libs for this might not be installed - that's ok, return nothing
        if(InkyImpressionDisplay.check_module_installed('inky')):
            # if passed return list of devices
            result = [f"{InkyDisplay.pkg_name}.impression"]

        return result

    def _display(self, image):
        # no palette adjustments need to be done as the Inky lib does them from the image
        self._device.set_image(image)
        self._device.show()

    def clear(self):
        from inky.inky_uc8159 import CLEAN

        for _ in range(2):
            for y in range(self.height - 1):
                for x in range(self.width - 1):
                    self._device.set_pixel(x, y, CLEAN)

        self._device.show()
