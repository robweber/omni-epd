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
import logging
import json
from PIL import Image, ImageEnhance
from . conf import IMAGE_DISPLAY, IMAGE_ENHANCEMENTS


class VirtualEPD:
    """
    VirtualEPD is a wrapper class for a device, or family of devices, that all use the same display code
    New devices should extend this class and implement the, at a minimum, the following:

    pkg_name = set this to the package name of the concrete class
    width = width of display, can set in __init__
    height = height of display, can set in __init__
    get_supported_devices() = must return a list of supported devices for this class in the format {pkgname.devicename}
    _display() = performs the action of writing the image to the display
    """

    pkg_name = "virtualdevice"  # the package name of the concrete class
    width = 0   # width of display
    height = 0  # height of display
    _device = None  # concrete device class, initialize in __init__
    _config = None  # configuration options passed in via dict at runtime or .ini file
    __device_name = ""  # name of this device

    def __init__(self, deviceName, config):
        self._config = config
        self.__device_name = deviceName

        self._logger = logging.getLogger(self.__str__())

    def __str__(self):
        return f"{self.pkg_name}.{self.__device_name}"

    def __generate_palette(self, pstr):
        result = []
        pjson = json.loads(pstr)

        for c in pjson:
            result += [int(c[0]), int(c[1]), int(c[2])]

        return result

    def __applyConfig(self, image):
        """
        Apply any values passed in from the global configuration that should
        apply to all images before writing to the epd
        """

        if(self._config.has_option(IMAGE_DISPLAY, "rotate")):
            image = image.rotate(self._config.getfloat(IMAGE_DISPLAY, "rotate"))
            self._logger.debug(f"Rotating image {self._config.getfloat(IMAGE_DISPLAY, 'rotate')}")

        if(self._config.has_option(IMAGE_DISPLAY, "flip_horizontal") and self._config.getboolean(IMAGE_DISPLAY, "flip_horizontal")):
            image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
            self._logger.debug("Flipping image horizontally")

        if(self._config.has_option(IMAGE_DISPLAY, "flip_vertical") and self._config.getboolean(IMAGE_DISPLAY, "flip_vertical")):
            image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
            self._logger.debug("Flipping image vertically")

        # must be one of the valid PILLOW modes, and display must support
        # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
        if(self._config.has_option(IMAGE_ENHANCEMENTS, "color")):
            # if total_colors given filter down to this many colors only
            if(self._config.get(IMAGE_ENHANCEMENTS, "color") == 'P' and self._config.has_option(IMAGE_ENHANCEMENTS, 'total_colors')):
                total_colors = self._config.getint(IMAGE_ENHANCEMENTS, "total_colors")
                image = image.convert(self._config.get(IMAGE_ENHANCEMENTS, "color"), palette=Image.ADAPTIVE,
                                      colors=total_colors)
                self._logger.debug(f"Applying color mode: {self._config.get(IMAGE_ENHANCEMENTS, 'color')} with {total_colors} colors")
            # if palette given filter out all colors but these
            elif(self._config.get(IMAGE_ENHANCEMENTS, "color") == 'P' and self._config.has_option(IMAGE_ENHANCEMENTS, 'palette')):
                # load the palette as a list from the string
                palette = self.__generate_palette(self._config.get(IMAGE_ENHANCEMENTS, "palette"))

                # create a new image to define the palette
                palette_image = Image.new("P", (1, 1))

                # set the palette, set all other colors to 0
                palette_image.putpalette(palette + [0, 0, 0] * (256-len(palette)))

                # load image so it can be processed
                image.load()
                image = image._new(image.im.convert('P', True, palette_image.im)).convert('RGB')

                self._logger.debug(f"Applying color mode: {self._config.get(IMAGE_ENHANCEMENTS, 'color')} with custom palette")
            else:
                # just apply the color enhancment mode
                image = image.convert(self._config.get(IMAGE_ENHANCEMENTS, "color"))
                self._logger.debug(f"Applying color mode: {self._config.get(IMAGE_ENHANCEMENTS, 'color')}")

        if(self._config.has_option(IMAGE_ENHANCEMENTS, "contrast")):
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(self._config.getfloat(IMAGE_ENHANCEMENTS, "contrast"))
            self._logger.debug(f"Applying contrast: {self._config.getfloat(IMAGE_ENHANCEMENTS, 'contrast')}")

        if(self._config.has_option(IMAGE_ENHANCEMENTS, "brightness")):
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(self._config.getfloat(IMAGE_ENHANCEMENTS, "brightness"))
            self._logger.debug(f"Applying brightness: {self._config.getfloat(IMAGE_ENHANCEMENTS, 'brightness')}")

        if(self._config.has_option(IMAGE_ENHANCEMENTS, "sharpness")):
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(self._config.getfloat(IMAGE_ENHANCEMENTS, "sharpness"))
            self._logger.debug(f"Applying sharpness: {self._config.getfloat(IMAGE_ENHANCEMENTS, 'sharpness')}")

        return image

    # helper method to load a concrete display object based on the package and class name
    def load_display_driver(self, packageName, className):
        try:
            # load the given driver module
            driver = importlib.import_module(f"{packageName}.{className}")
        except ModuleNotFoundError:
            # hard stop if driver not
            print(f"{packageName}.{className} not found, refer to install instructions")
            exit(2)

        return driver

    # REQUIRED - a list of devices supported by this class, format is {pkgname.devicename}
    @staticmethod
    def get_supported_devices():
        raise NotImplementedError

    # REQUIRED - actual display code, PIL image given
    def _display(self, image):
        raise NotImplementedError

    # OPTIONAL - run at the top of each update to do required pre-work
    def prepare(self):
        return True

    # DON'T override this method directly, use _display()
    def display(self, image):
        self._display(self.__applyConfig(image))

    # OPTIONAL - put the display to sleep after each update, if device supports
    def sleep(self):
        return True

    # OPTIONAL - clear the display, if device supports
    def clear(self):
        return True

    # OPTIONAL close out the device, called when the program ends
    def close(self):
        return True
