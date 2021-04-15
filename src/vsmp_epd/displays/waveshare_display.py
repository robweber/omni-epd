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

import importlib
from pkgutil import iter_modules
from waveshare_epd import epdconfig
from .. virtualepd import VirtualEPD


class WaveshareDisplay(VirtualEPD):
    pkg_name = 'waveshare_epd'

    def __init__(self, deviceName):
        super(WaveshareDisplay, self).__init__(f"{deviceName}")

        # load the module
        deviceObj = self.load_display_driver(self.pkg_name, deviceName)

        # create the epd object
        self._device = deviceObj.EPD()

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        result = []

        try:
            # load the waveshare library
            waveshareModule = importlib.import_module(WaveshareDisplay.pkg_name)

            # return a list of all submodules (device types)
            result = [f"{WaveshareDisplay.pkg_name}.{s.name}" for s in iter_modules(waveshareModule.__path__) if s.name != 'epdconfig']
        except ModuleNotFoundError:
            # python libs for this might not be installed - that's ok, return nothing
            pass

        return result

    def prepare(self):
        self._device.init()

    def display(self, image):
        self._device.display(self._device.getbuffer(image))

    def sleep(self):
        self._device.sleep()

    def clear(self):
        return True

    def close(self):
        epdconfig.module_init()
        epdconfig.module_exit()
