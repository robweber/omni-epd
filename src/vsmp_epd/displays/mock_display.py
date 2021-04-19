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

import logging
from .. virtualepd import VirtualEPD


class MockDisplay(VirtualEPD):
    """
    This is a reference implementation of a display extending VirtualEPD
    it does not physically write to anything but can be used as a mock testing device
    """

    pkg_name = 'vsmp_epd'

    def __init__(self, deviceName, config):
        super(MockDisplay, self).__init__(deviceName, config)

        # this is normally where you'd load actual device class but nothing to load here

        # set the width and height - doesn't matter since we won't write anything
        self.width = 100
        self.height = 100

    @staticmethod
    def get_supported_devices():
        # only one display supported, the test display
        return [f"{MockDisplay.pkg_name}.mock"]

    def prepare(self):
        logging.info(f"preparing {self.__str__()}")

    def _display(self, image):
        logging.info(f"writing image to {self.__str__()}")

    def sleep(self):
        logging.info(f"{self.__str__()} is sleeping")

    def clear(self):
        logging.info(f"clearing {self.__str__()}")

    def close(self):
        logging.info(f"closing {self.__str__()}")
