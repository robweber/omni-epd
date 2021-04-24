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
import os.path
from .. virtualepd import VirtualEPD


class MockDisplay(VirtualEPD):
    """
    This is a reference implementation of a display extending VirtualEPD
    it does not physically write to anything but can be used as a mock testing device
    """

    pkg_name = 'omni_epd'
    output_file = 'mock_output.jpg'

    def __init__(self, deviceName, config):
        super(MockDisplay, self).__init__(deviceName, config)

        self.logger = logging.getLogger(__name__)

        # this is normally where you'd load actual device class but nothing to load here

        # set location to write test image
        self.output_file = os.path.join(os.getcwd(), self.output_file)

        # set the width and height - doesn't matter since we won't write anything
        self.width = 400
        self.height = 200

    @staticmethod
    def get_supported_devices():
        # only one display supported, the test display
        return [f"{MockDisplay.pkg_name}.mock"]

    def prepare(self):
        self.logger.info(f"preparing {self.__str__()}")

    def _display(self, image):
        self.logger.info(f"{self.__str__()} writing image to {self.output_file}")
        image.save(self.output_file, "JPEG")

    def sleep(self):
        self.logger.info(f"{self.__str__()} is sleeping")

    def clear(self):
        self.logger.info(f"clearing {self.__str__()}")

    def close(self):
        self.logger.info(f"closing {self.__str__()}")
