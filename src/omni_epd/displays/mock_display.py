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
    it can write images to a testing file for use as a mock testing device
    """

    pkg_name = 'omni_epd'
    output_file = 'mock_output.jpg'

    def __init__(self, deviceName, config):
        super(MockDisplay, self).__init__(deviceName, config)

        self.logger = logging.getLogger(__name__)

        # this is normally where you'd load actual device class but nothing to load here

        # set location to write test image - can be set in config file
        self.output_file = self._get_device_option("file", os.path.join(os.getcwd(), self.output_file))

        # set the width and height
        self.width = 400
        self.height = 200

        # this object can also work in color mode
        self._modes_available = ('bw', 'color')

    @staticmethod
    def get_supported_devices():
        # only one display supported, the test display
        return [f"{MockDisplay.pkg_name}.mock"]

    def prepare(self):
        self.logger.info(f"preparing {self.__str__()}")

    def _display(self, image):
        if(self._getboolean_device_option('write_file', True)):
            self.logger.info(f"{self.__str__()} writing image to {self.output_file}")

            if(image.mode == 'P'):
                # can't write P mode images
                image = image.convert('RGB')

            image.save(self.output_file, "JPEG")
        else:
            self.logger.info(f"{self.__str__()} display() called, skipping output")

    def sleep(self):
        self.logger.info(f"{self.__str__()} is sleeping")

    def clear(self):
        self.logger.info(f"clearing {self.__str__()}")

    def close(self):
        self.logger.info(f"closing {self.__str__()}")
