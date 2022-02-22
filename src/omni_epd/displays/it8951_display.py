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
    This will communicate with IT8951 type displays utilzing the driver built by Greg GregDMeyer
    https://github.com/GregDMeyer/IT8951
    """

    pkg_name = 'IT8951'
    it8951_constants = None

    def __init__(self, deviceName, config):
        super().__init__(deviceName, config)

        self.logger = logging.getLogger(__name__)

        # load the IT8951.display package and create the object
        deviceObj = self.load_display_driver(self.pkg_name, "display")
        self._device = deviceObj.AutoEPDDisplay(vcom=self._getfloat_device_option('vcom', -2.06),
                                                spi_hz=self._getint_device_option('spi_hz', 24000000),
                                                rotate=self._get_device_option('rotate', None))

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

        # load the from IT8951.constants
        self.it8951_constants = self.load_display_driver(self.pkg_name, "constants")

    @staticmethod
    def get_supported_devices():
        # only one display supported, the test display
        return [f"{IT8951Display.pkg_name}.it8951"]

    def prepare(self):
        self.logger.info(f"preparing {self.__str__()}")
        self._device.epd.run()

    def _display(self, image):
        # keep this as it applies any filters defined in INI file
        image = self._filterImage(image)

        self.clear()  # not sure if this is needed, was part of example

        dims = (self.width, self.height)
        image.thumbnail(dims)

        paste_coords = [dims[i] - image.size[i] for i in (0,1)]  # align image with bottom of display

        # write image to display
        self._device.frame_buf.paste(pil_im, paste_coords)
        self._device.draw_full(it8951_constants.DisplayModes.GC16)

        self.logger.info(f"{self.__str__()} writing image to EPD")

    def sleep(self):
        self.logger.info(f"{self.__str__()} is sleeping")
        self._device.epd.sleep()

    def clear(self):
        self.logger.info(f"clearing {self.__str__()}")
        self._device.clear()

    def close(self):
        self.logger.info(f"closing {self.__str__()}")
        # doesn't appear to be a close method for this EPD
