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
        super().__init__(f"{deviceName}", config)

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
        result = []

        # list of common devices that share init() and display() method calls
        commonDeviceList = ["epd1in54_V2", "epd2in13d",
                            "epd2in9_V2", "epd2in9d",
                            "epd5in83", "epd5in83_V2",
                            "epd7in5", "epd7in5_HD", "epd7in5_V2"]

        # python libs for this might not be installed - that's ok, return nothing
        if(WaveshareDisplay.check_module_installed('waveshare_epd')):
            result = WaveshareDisplay.lutInitList + WaveshareDisplay.modeInitList + commonDeviceList

            # return a list of all submodules (device types)
            result = [f"{WaveshareDisplay.pkg_name}.{n}" for n in result]

        return result

    def prepare(self):
        # if device needs an init param
        if(self.alt_init):
            self._device.init(self.alt_init_param)
        else:
            self._device.init()

    def _display(self, image):
        # no need to adjust palette, done in waveshare driver
        self._device.display(self._device.getbuffer(image))

    def sleep(self):
        self._device.sleep()

    def clear(self):
        self._device.Clear()

    def close(self):
        epdconfig = self.load_display_driver(self.pkg_name, 'epdconfig')
        epdconfig.module_init()
        epdconfig.module_exit()


class WaveshareTriColorDisplay(VirtualEPD):
    """
    This class is for the Waveshare displays that support 3 colors
    typically white/black/red or white/black/yellow
    https://github.com/waveshare/e-Paper
    """

    pkg_name = 'waveshare_epd'
    max_colors = 3

    # list of all devices - some drivers cover more than one device
    deviceMap = {"epd1in54b": {"driver": "epd1in54b", "modes": ("bw", "red")},
                 "epd1in54b_V2": {"driver": "epd1in54b_V2", "modes": ("bw", "red")},
                 "epd1in54c": {"driver": "epd1in54c", "modes": ("bw", "yellow")},
                 "epd2in13b": {"driver": "epd2in13bc", "modes": ("bw", "red")},
                 "epd2in13b_V3": {"driver": "epd2in13b_V3", "modes": ("bw", "red")},
                 "epd2in13c": {"driver": "epd2in13bc", "modes": ("bw", "yellow")},
                 "epd2in66b": {"driver": "epd2in66b", "modes": ("bw", "red")},
                 "epd2in7b": {"driver": "epd2in7b", "modes": ("bw", "red")},
                 "epd2in7b_V2": {"driver": "epd2in7b_V2", "modes": ("bw", "red")},
                 "epd2in9b": {"driver": "epd2in9bc", "modes": ("bw", "red")},
                 "epd2in9b_V3": {"driver": "epd2in9b_V3", "modes": ("bw", "red")},
                 "epd2in9c": {"driver": "epd2in9bc", "modes": ("bw", "yellow")},
                 "epd4in2bc": {"driver": "epd4in2bc", "modes": ("bw", "red")},
                 "epd4in2c": {"driver": "epd4in2bc", "modes": ("bw", "yellow")},
                 "epd4in2b_V2": {"driver": "epd4in2b_V2", "modes": ("bw", "red")},
                 "epd5in83b": {"driver": "epd5in83bc", "modes": ("bw", "red")},
                 "epd5in83c": {"driver": "epd5in83bc", "modes": ("bw", "yellow")},
                 "epd5in83b_V2": {"driver": "epd5in83b_V2", "modes": ("bw", "red")},
                 "epd7in5b": {"driver": "epd7in5bc", "modes": ("bw", "red")},
                 "epd7in5c": {"driver": "epd7in5bc", "modes": ("bw", "yellow")},
                 "epd7in5b_V2": {"driver": "epd7in5b_V2", "modes": ("bw", "red")},
                 "epd7in5b_HD": {"driver": "epd7in5b_HD", "modes": ("bw", "red")}}

    def __init__(self, deviceName, config):
        super().__init__(deviceName, config)

        # load driver based on name from deviceMap dict
        deviceObj = self.load_display_driver(self.pkg_name, self.deviceMap[deviceName]["driver"])

        # create the epd object
        self._device = deviceObj.EPD()

        # set the allowed modes
        self.modes_available = self.deviceMap[deviceName]['modes']

        if(self.mode == 'red'):
            self.palette_filter.append([255, 0, 0])
        elif(self.mode == 'yellow'):
            self.palette_filter.append([255, 255, 0])

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        result = []

        # python libs for this might not be installed - that's ok, return nothing
        if(WaveshareTriColorDisplay.check_module_installed('waveshare_epd')):
            result = [f"{WaveshareTriColorDisplay.pkg_name}.{n}" for n in WaveshareTriColorDisplay.deviceMap]

        return result

    def prepare(self):
        self._device.init()

    def _display(self, image):

        if(self.mode == 'bw'):
            # send the black/white image and blank second image (safer since some drivers require data)
            self._device.display(self._device.getbuffer(image), [0x00] * (int(self.width/8) * self.height))
        else:
            # apply the color filter to get a 3 color image
            image = self._filterImage(image)

            # separate out black from the other color
            img_black = image.copy()
            img_black.putpalette((255, 255, 255, 0, 0, 0, 255, 255, 255) + (0, 0, 0)*253)

            img_color = image.copy()
            img_color.putpalette((255, 255, 255, 255, 255, 255, 0, 0, 0) + (0, 0, 0)*253)

            self._device.display(self._device.getbuffer(img_black), self._device.getbuffer(img_color))

    def sleep(self):
        self._device.sleep()

    def clear(self):
        self._device.Clear()

    def close(self):
        epdconfig = self.load_display_driver(self.pkg_name, 'epdconfig')
        epdconfig.module_init()
        epdconfig.module_exit()


class WaveshareGrayscaleDisplay(VirtualEPD):
    """
    This class is for the Waveshare displays that support 4 shade grayscale

    https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd2in7.py
    https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd3in7.py
    https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd4in2.py
    """

    pkg_name = 'waveshare_epd'
    modes_available = ("bw", "gray4")
    max_colors = 4

    deviceList = ["epd2in7", "epd3in7", "epd4in2"]  # devices that support 4 shade grayscale

    def __init__(self, deviceName, config):
        super().__init__(deviceName, config)

        deviceObj = self.load_display_driver(self.pkg_name, deviceName)

        # create the epd object
        self._device = deviceObj.EPD()

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        result = []

        if(WaveshareGrayscaleDisplay.check_module_installed('waveshare_epd')):
            result = [f"{WaveshareGrayscaleDisplay.pkg_name}.{n}" for n in WaveshareGrayscaleDisplay.deviceList]

        return result

    def prepare(self):
        # 3.7 in has different init methods
        if(self._device_name == "epd3in7"):
            if(self.mode == 'gray4'):
                self._device.init(0)
            else:
                self._device.init(1)
        else:
            if(self.mode == "gray4"):
                self._device.Init_4Gray()
            else:
                self._device.init()

    def _display(self, image):
        # no need to adjust image, done in waveshare lib

        if(self.mode == "gray4"):
            self._device.display_4Gray(self._device.getbuffer_4Gray(image))
        else:
            # 3.7 in has different bw method
            if(self._device_name == "epd3in7"):
                self._device.display_1Gray(self._device.getbuffer(image))
            else:
                self._device.display(self._device.getbuffer(image))

    def sleep(self):
        self._device.sleep()

    def clear(self):
        self._device.Clear()

    def close(self):
        epdconfig = self.load_display_driver(self.pkg_name, 'epdconfig')
        epdconfig.module_init()
        epdconfig.module_exit()


class Waveshare102inDisplay(VirtualEPD):
    """
    This class is for the Waveshare 1.02 in display only as it has some method calls that are different
    https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd1in02.py
    """

    pkg_name = 'waveshare_epd'

    def __init__(self, deviceName, config):
        super().__init__(deviceName, config)

        deviceObj = self.load_display_driver(self.pkg_name, deviceName)

        # create the epd object
        self._device = deviceObj.EPD()

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        result = []

        if(Waveshare102inDisplay.check_module_installed('waveshare_epd')):
            result = [f"{Waveshare102inDisplay.pkg_name}.epd1in02"]

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
        epdconfig = self.load_display_driver(self.pkg_name, 'epdconfig')
        epdconfig.module_init()
        epdconfig.module_exit()


class WaveshareMultiColorDisplay(VirtualEPD):
    """
    This class is for the Waveshare 7 color displays
    https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd5in65f.py
    https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/.py
    """

    pkg_name = 'waveshare_epd'
    max_colors = 7
    modes_available = ('bw', 'color')

    deviceList = ["epd5in64f", "epd4in01f"]

    def __init__(self, deviceName, config):
        super().__init__(deviceName, config)

        deviceObj = self.load_display_driver(self.pkg_name, deviceName)

        # create the epd object
        self._device = deviceObj.EPD()

        # set the width and height
        self.width = self._device.width
        self.height = self._device.height

    @staticmethod
    def get_supported_devices():
        result = []

        if(WaveshareMultiColorDisplay.check_module_installed('waveshare_epd')):
            result = [f"{WaveshareMultiColorDisplay.pkg_name}.{n}" for n in WaveshareMultiColorDisplay.deviceList]

        return result

    def prepare(self):
        self._device.init()

    def _display(self, image):
        # driver takes care of filtering when in color mode
        if(self.mode == 'bw'):
            image = self._applyFilter(image)

        self._device.display(self._device.getbuffer(image))

    def sleep(self):
        self._device.sleep()

    def clear(self):
        self._device.Clear()

    def close(self):
        epdconfig = self.load_display_driver(self.pkg_name, 'epdconfig')
        epdconfig.module_init()
        epdconfig.module_exit()
