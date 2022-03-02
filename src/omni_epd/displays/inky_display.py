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
from inky.inky_uc8159 import DESATURATED_PALETTE
from .. virtualepd import VirtualEPD
from .. conf import check_module_installed
INKY_PKG = "inky"


class InkyDisplay(VirtualEPD):
    """
    This is an abstraction for Pimoroni Inky pHat and wHat devices
    https://github.com/pimoroni/inky
    """

    pkg_name = INKY_PKG
    mode = "black"  # default mode is black
    modes_available = ("black")

    deviceList = ["phat_black", "phat_red", "phat_yellow",
                    "phat1608_black", "phat1608_red", "phat1608_yellow",
                    "what_black", "what_red", "what_yellow", "auto", 
                    "impression"]

    def __init__(self, deviceName, config):
        super().__init__(deviceName, config)

        # need to figure out what type of device we have
        dType, dColor, *_ = deviceName.split('_') + [None]

        self._device, self.clear_color, dColor = self.load_device(dType, dColor)

        # set mode to black + any other color supported
        if(self.mode != "black"):
            self.modes_available = ('black', dColor)

        # phat and what devices expect colors in the order white, black, other
        if(self.mode == "red" and dColor == "red"):
            self.palette_filter.append([255, 0, 0])
            self.max_colors = 3
        elif(self.mode == "yellow" and dColor == "yellow"):
            self.palette_filter.append([255, 255, 0])
            self.max_colors = 3
        elif(self.mode == "color" and dColor == "color"):
            self.palette_filter = DESATURATED_PALETTE
            self.max_colors = 8

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    def load_device(self, dType, dColor):
        if(dType == 'phat'):
            deviceObj = self.load_display_driver(self.pkg_name, 'phat')
            device = deviceObj.InkyPHAT(dColor)
        elif(dType == 'phat1608'):
            deviceObj = self.load_display_driver(self.pkg_name, 'phat')
            device = deviceObj.InkyPHAT_SSD1608(dColor)
        elif(dType == 'what'):
            deviceObj = self.load_display_driver(self.pkg_name, 'what')
            device = deviceObj.InkyWHAT(dColor)
        elif(dType == 'impression'):
            deviceObj = self.load_display_driver(self.pkg_name, 'inky_uc8159')
            device = deviceObj.Inky()
        elif(dType == 'auto'):
            deviceObj = self.load_display_driver(self.pkg_name, 'auto')
            device = deviceObj.auto()

        if(device.colour == 'multi'):
            return device, device.CLEAN, 'color'
        else:
            return device, device.WHITE, dColor

    @staticmethod
    def get_supported_devices():
        return [] if not check_module_installed(INKY_PKG) else [f"{INKY_PKG}.{n}" for n in InkyDisplay.deviceList]

    # set the image and display
    def _display(self, image):
        # set border
        self._device.set_border(getattr(self._device, self._get_device_option('border', '').upper(), self._device.border_colour))

        # apply any needed conversions to this image based on the mode
        if(self.mode == 'color'):
            saturation = self._getfloat_device_option('saturation', .5)  # .5 is default from Inky lib
            self._device.set_image(image.convert("RGB"), saturation=saturation)
        else:
            image = self._filterImage(image)
            self._device.set_image(image.convert("RGB"))

        self._device.show()

    def clear(self):
        for _ in range(2):
            for y in range(self.height - 1):
                for x in range(self.width - 1):
                    self._device.set_pixel(x, y, self.clear_color)

        self._device.show()


# left here for back-compat
class InkyImpressionDisplay(InkyDisplay):
    @staticmethod
    def get_supported_devices():
        return []

    devices = []  # allow base to handle them all

    def __init__(self, deviceName, config):
        super().__init__(deviceName, config)