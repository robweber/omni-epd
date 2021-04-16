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

from .. virtualepd import VirtualEPD
from inky import InkyPHAT, InkyWHAT, WHITE


class InkyDisplay(VirtualEPD):
    pkg_name = 'inky'

    def __init__(self, deviceName):
        super(InkyDisplay, self).__init__(deviceName)

        # need to figure out what type of device we have
        dType, dColor = deviceName.split('_')

        if(dType == 'phat'):
            self._device = InkyPHAT(dColor)
        elif(dType == 'what'):
            self._device = InkyWHAT(dColor)

        # set the width and height - doesn't matter since we won't write anything
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        return [f"{InkyDisplay.pkg_name}.{n}" for n in ["phat_black", "phat_red", "phat_yellow", "what_black", "what_red", "what_yellow"]]

    def display(self, image):
        self._device.set_image(image)
        self._device.show()

    def clear(self):
        for _ in range(2):
            for y in range(self.height - 1):
                for x in range(self.width - 1):
                    self._device.set_pixel(x, y, WHITE)

        self._device.show()
