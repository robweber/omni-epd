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

import logging
from .. virtualepd import VirtualEPD


class IT8951Display(VirtualEPD):
    """
    This is a reference implementation of a display extending VirtualEPD
    it can write images to a testing file for use as a mock testing device
    """

    pkg_name = 'waveshare_epd'
    max_colors = 256
    modes_available = ('bw', 'color', 'palette')

    def __init__(self, deviceName, config):
        super().__init__(deviceName, config)

        self.logger = logging.getLogger(__name__)

        # this is normally where you'd load actual device class

        # set the width and height
        self.width = 400
        self.height = 200

    @staticmethod
    def get_supported_devices():
        # only one display supported, the test display
        return [f"{IT8951Display.pkg_name}.it8951"]

    def prepare(self):
        self.logger.info(f"preparing {self.__str__()}")

    def _display(self, image):
        # keep this as it applies any filters defined in INI file
        image = self._filterImage(image)

        self.logger.info(f"{self.__str__()} writing image to EPD")

    def sleep(self):
        self.logger.info(f"{self.__str__()} is sleeping")

    def clear(self):
        self.logger.info(f"clearing {self.__str__()}")

    def close(self):
        self.logger.info(f"closing {self.__str__()}")
