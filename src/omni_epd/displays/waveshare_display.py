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

import importlib
from pkgutil import iter_modules
from .. virtualepd import VirtualEPD


class WaveshareDisplay(VirtualEPD):
    """
    This is an abstraction for Waveshare EPD devices that are single color only
    https://github.com/waveshare/e-Paper
    """

    pkg_name = 'waveshare_epd'

    # devices that use alternate init methods
    lutInitList = ["epd2in9", "epd2in13", "epd1in54"]
    modeInitList = ["epd2in66", "epd2in13_V2"]

    alt_init = False  # specify that init with a param should be used
    alt_init_param = 0  # the parameter to pass to init - specifies update mode (full vs partial)

    def __init__(self, deviceName, config):
        super(WaveshareDisplay, self).__init__(f"{deviceName}", config)

        # load the module
        deviceObj = self.load_display_driver(self.pkg_name, deviceName)

        # create the epd object
        self._device = deviceObj.EPD()

        # check if alternate init method is used
        if(deviceName in self.lutInitList or deviceName in self.modeInitList):
            self.alt_init = True

            # some devices set the full instruction as the param
            if(deviceName in self.lutInitList):
                self.alt_init_param = self._device.lut_full_update

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        result = WaveshareDisplay.lutInitList + WaveshareDisplay.modeInitList

        # list of common devices that share init() and display() method calls
        commonDeviceList = ["epd1in54_V2", "epd2in13d", "epd2in7",
                      "epd2in9_V2", "epd2in9d", "epd4in01f",
                      "epd4in2", "epd5in65f", "epd5in83",
                      "epd5in83_V2", "epd7in5", "epd7in5_HD", "epd7in5_V2"]
        try:
            # load the waveshare library
            from waveshare_epd import epdconfig

            result = result + commonDeviceList

            # return a list of all submodules (device types)
            result = [f"{WaveshareDisplay.pkg_name}.{n}" for n in result]
        except ModuleNotFoundError:
            # python libs for this might not be installed - that's ok, return nothing
            pass

        return result

    def prepare(self):

        # if device needs an init param
        if(self.alt_init):
            self._device.init(self.alt_init_param)
        else:
            self._device.init()

    def _display(self, image):
        self._device.display(self._device.getbuffer(image))

    def sleep(self):
        self._device.sleep()

    def clear(self):
        self._device.Clear()

    def close(self):
        # can't import this earlier as pkg may not be installed
        from waveshare_epd import epdconfig
        epdconfig.module_init()
        epdconfig.module_exit()

class Waveshare102inDisplay(VirtualEPD):
    """
    This class is for the Waveshare 1.02 in display only as it has some method calls that are different
    https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd1in02.py
    """

    pkg_name = 'waveshare_epd'

    def __init__(self, deviceName, config):
        super(MockDisplay, self).__init__(deviceName, config)

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
            from waveshare_epd import epdconfig

            result = [f"{Waveshare102inDisplay.pkg_name}.epd1in02"]
        except ModuleNotFoundError:
            # python libs for this might not be installed - that's ok, return nothing
            pass

        return result

    def prepare(self):
        self._device.Init()

    def _display(self, image):
        self._device.Display(self._device.getbuffer(image))

    def sleep(self):
        self._device.Sleep()

    def clear(self):
        self._device.Clear()

    def close(self):
        # can't import this earlier as pkg may not be installed
        from waveshare_epd import epdconfig
        epdconfig.module_init()
        epdconfig.module_exit()

class Waveshare3in7Display(VirtualEPD):
    """
    This class is for the Waveshare 3.7in display only as it
    has support for different gray scales and the methods are different
    https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd3in7.py
    """

    pkg_name = 'waveshare_epd'

    def __init__(self, deviceName, config):
        super(MockDisplay, self).__init__(deviceName, config)

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
            from waveshare_epd import epdconfig

            result = [f"{Waveshare102inDisplay.pkg_name}.epd3in7"]
        except ModuleNotFoundError:
            # python libs for this might not be installed - that's ok, return nothing
            pass

        return result

    def prepare(self):
        # only b/w supported right now
        self._device.init(1)

    def _display(self, image):
        self._device.display_1Gray(self._device.getbuffer(image))

    def sleep(self):
        self._device.sleep()

    def clear(self):
        self._device.Clear()

    def close(self):
        # can't import this earlier as pkg may not be installed
        from waveshare_epd import epdconfig
        epdconfig.module_init()
        epdconfig.module_exit()
