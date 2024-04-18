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

import json
import importlib
import logging
import subprocess
import io
import re
import itertools
from importlib import resources
from PIL import Image, ImageEnhance, ImageColor
from . conf import EPD_CONFIG, IMAGE_DISPLAY, IMAGE_ENHANCEMENTS
from . errors import EPDConfigurationError


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
    mode = "bw"  # mode of the display, bw by default, others defined by display class
    modes_available = ("bw")  # modes this display supports, set in __init__

    # only used by displays that need palette filtering before sending to display driver
    max_colors = 2  # assume only b+w supported by default, set in __init__
    palette_filter = [[255, 255, 255], [0, 0, 0]]  # assume only b+w supported by default, set in __init__

    _device = None  # concrete device class, initialize in __init__
    _config = None  # configuration options passed in via dict at runtime or .ini file
    _device_name = ""  # name of this device

    def __init__(self, deviceName, config):
        self._config = config
        self._device_name = deviceName

        self._logger = logging.getLogger(self.__str__())

        # set the display mode
        self.mode = self._get_device_option('mode', self.mode)

        if (self.mode == 'black'):
            self._logger.warn("The mode 'black' is deprecated, 'bw' should be used instead. This will be removed in a future release.")
            self.mode = 'bw'

    def __str__(self):
        return f"{self.pkg_name}.{self._device_name}"

    def __parse_palette(self, color_str):
        """ parse the color infomration to return a RGB color from a color string
        :param color_str: the color as either a hex value (#000000), RGB list [R,G,B] or color name (blue, red)
        :raises ValueError: if the color string is in an invalid format

        :returns: the color_str converted to a list of RGB values
        """
        if re.match(r'#[a-fA-F0-9]{6}', color_str) or color_str.lower() in ImageColor.colormap:
            return ImageColor.getrgb(color_str)
        elif re.match(r'\[?(\d{1,3}),(\d{1,3}),(\d{1,3})\]?', color_str):
            return list(map(int, re.findall(r'\d{1,3}', color_str)))
        else:
            raise ValueError(f"Invalid color format: {color_str}")

    def __generate_palette(self, colors):
        """ generate a palette given the colors available for this display
        :param colors: a list of valid colors as a string

        :returns: a single list of integers representing an RGB value for each color
        """
        result = colors.replace(" ", "")
        result = re.findall(fr'#[a-fA-F0-9]{{6}}|\[?\d{{1,3}},\d{{1,3}},\d{{1,3}}\]?|{"|".join(ImageColor.colormap.keys())}', result, re.IGNORECASE)
        result = list(itertools.chain.from_iterable(map(self.__parse_palette, result)))

        return result

    def __applyConfig(self, image):
        """
        Apply any values passed in from the global configuration that should
        apply to all images before writing to the epd

        :param image: an Image object

        :returns: the modified image
        """

        if (self._config.has_option(IMAGE_DISPLAY, "rotate")):
            image = image.rotate(self._config.getfloat(IMAGE_DISPLAY, "rotate"))
            self._logger.debug(f"Rotating image {self._config.getfloat(IMAGE_DISPLAY, 'rotate')}")

        if (self._config.has_option(IMAGE_DISPLAY, "flip_horizontal") and self._config.getboolean(IMAGE_DISPLAY, "flip_horizontal")):
            image = image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
            self._logger.debug("Flipping image horizontally")

        if (self._config.has_option(IMAGE_DISPLAY, "flip_vertical") and self._config.getboolean(IMAGE_DISPLAY, "flip_vertical")):
            image = image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
            self._logger.debug("Flipping image vertically")

        if (self._config.has_option(IMAGE_ENHANCEMENTS, "contrast")):
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(self._config.getfloat(IMAGE_ENHANCEMENTS, "contrast"))
            self._logger.debug(f"Applying contrast: {self._config.getfloat(IMAGE_ENHANCEMENTS, 'contrast')}")

        if (self._config.has_option(IMAGE_ENHANCEMENTS, "brightness")):
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(self._config.getfloat(IMAGE_ENHANCEMENTS, "brightness"))
            self._logger.debug(f"Applying brightness: {self._config.getfloat(IMAGE_ENHANCEMENTS, 'brightness')}")

        if (self._config.has_option(IMAGE_ENHANCEMENTS, "sharpness")):
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(self._config.getfloat(IMAGE_ENHANCEMENTS, "sharpness"))
            self._logger.debug(f"Applying sharpness: {self._config.getfloat(IMAGE_ENHANCEMENTS, 'sharpness')}")

        if (self._config.has_option(IMAGE_DISPLAY, "dither") and self._config.get(IMAGE_DISPLAY, "dither")):
            dither = self._config.get(IMAGE_DISPLAY, "dither").lower().replace("sierra-2-4a", "sierralite").replace("-", "")
            image = self._ditherImage(image, dither)
            self._logger.debug(f"Applying dither: {dither}")

        return image

    """
    helper methods to get custom config options, providing a fallback if needed
    avoids having to do constant has_option(), get() calls within device class
    """
    def _get_device_option(self, option, fallback):
        # if exists in local config use that, otherwise check EPD section
        if (self._config.has_option(self.getName(), option)):
            return self._config.get(self.getName(), option)
        else:
            return self._config.get(EPD_CONFIG, option, fallback=fallback)

    def _getint_device_option(self, option, fallback):
        # if exists in local config use that, otherwise check EPD section
        if (self._config.has_option(self.getName(), option)):
            return self._config.getint(self.getName(), option)
        else:
            return self._config.getint(EPD_CONFIG, option, fallback=fallback)

    def _getfloat_device_option(self, option, fallback):
        # if exists in local config use that, otherwise check EPD section
        if (self._config.has_option(self.getName(), option)):
            return self._config.getfloat(self.getName(), option)
        else:
            return self._config.getfloat(EPD_CONFIG, option, fallback=fallback)

    def _getboolean_device_option(self, option, fallback):
        # if exists in local config use that, otherwise check EPD section
        if (self._config.has_option(self.getName(), option)):
            return self._config.getboolean(self.getName(), option)
        else:
            return self._config.getboolean(EPD_CONFIG, option, fallback=fallback)

    def _filterImage(self, image, dither=Image.Dither.FLOYDSTEINBERG, force_palette=False):
        """ Converts image to b/w or attempts a palette filter based on allowed colors in the display
        :param image: an Image object
        :param dither: a valid dither technique, default is FLOYDSTEINBERG

        :raises EPDConfigurationError: if more colors are given in the palette than the display can support
        :returns: the image with the palette filtering applied
        """
        if (self.mode == 'bw' and not force_palette):
            image = image.convert("1", dither=dither)
        else:
            # load palette as string - this is a catch in case it was changed by the user
            colors = self._get_device_option('palette_filter', json.dumps(self.palette_filter))
            palette = self.__generate_palette(colors)

            # check if we have too many colors in the palette (*3 values for each color)
            if (len(palette) > self.max_colors * 3):
                raise EPDConfigurationError(self.getName(), "palette_filter", f"{int(len(palette)/3)} colors")

            # create a new image to define the palette
            palette_image = Image.new("P", (1, 1))

            # set the palette, set all other colors to 0
            palette_image.putpalette(palette + [0, 0, 0] * (256 - len(colors)))

            if (image.mode != 'RGB'):
                # convert to RGB as quantize requires it
                image = image.convert(mode='RGB')

            # apply the palette
            image = image.quantize(palette=palette_image, dither=dither)

        return image

    def _ditherImage(self, image, dither):
        """ apply a dithering effect to the image using the didder library
        https://github.com/robweber/omni-epd/wiki/Image-Dithering-Options
        :param image: an Image object
        :param dither: dithering effect as a string

        :returns: the image with the effect applied
        """
        dither_modes_ordered = ("clustereddot4x4", "clustereddotdiagonal8x8", "vertical5x3", "horizontal3x5",
                                "clustereddotdiagonal6x6", "clustereddotdiagonal8x8_2", "clustereddotdiagonal16x16",
                                "clustereddot6x6", "clustereddotspiral5x5", "clustereddothorizontalline",
                                "clustereddotverticalline", "clustereddot8x8", "clustereddot6x6_2",
                                "clustereddot6x6_3", "clustereddotdiagonal8x8_3")

        dither_modes_diffusion = ("simple2d", "floydsteinberg", "falsefloydsteinberg", "jarvisjudiceninke", "atkinson",
                                  "stucki", "burkes", "sierra", "tworowsierra", "sierralite", "stevenpigeon", "sierra3",
                                  "sierra2", "sierra2_4a")

        if (self.mode == 'bw'):
            colors = [[255, 255, 255], [0, 0, 0]]
        else:
            # load palette - this is a catch in case it was changed by the user
            colors = json.loads(self._get_device_option('palette_filter', json.dumps(self.palette_filter)))

            # check if we have too many colors in the palette
            if (len(colors) > self.max_colors):
                raise EPDConfigurationError(self.getName(), "palette_filter", f"{len(colors)} colors")

        # format palette the way didder expects it
        palette = [",".join(map(str, x)) for x in colors]
        palette = " ".join(palette)

        with resources.path("omni_epd", "didder") as p:
            didder = p

        cmd = [didder, "--in", "-", "--out", "-", "--palette", palette]
        cmd += ["--strength", self._config.get(IMAGE_DISPLAY, 'dither_strength', raw=True, fallback='1.0')]

        if (dither == "none"):
            return self._filterImage(image, Image.Dither.NONE)
        elif (dither in dither_modes_ordered):
            cmd += ["odm", dither]
        elif (dither in dither_modes_diffusion):
            cmd += ["edm", dither]
        elif (dither == "bayer"):
            # dither_args: X,Y dimensions of bayer matrix - powers of two, 3x3, 3x5, or 5x3
            cmd += ["bayer", self._config.get(IMAGE_DISPLAY, 'dither_args', fallback='4,4')]
        elif (dither == "random"):
            # dither_args: min,max or min_r,max_r,min_g,max_g,min_b,max_b
            cmd += ["random", self._config.get(IMAGE_DISPLAY, 'dither_args', fallback='-0.5,0.5')]
        elif (dither == "customordered"):
            # dither_args: JSON file or string
            cmd += ["odm", self._config.get(IMAGE_DISPLAY, 'dither_args', fallback='')]
        elif (dither == "customdiffusion"):
            # dither_args: JSON file or string
            cmd += ["edm", self._config.get(IMAGE_DISPLAY, 'dither_args', fallback='')]

        if (cmd[-2] == "edm" and self._config.getboolean(IMAGE_DISPLAY, 'dither_serpentine', fallback=False)):
            cmd.insert(-1, "--serpentine")

        with io.BytesIO() as buf:
            image.save(buf, "PNG")
            proc = subprocess.run(cmd, input=buf.getvalue(), capture_output=True)

        if (proc.returncode):
            self._logger.error(proc.stdout.decode().strip())
            return image

        with io.BytesIO(proc.stdout) as buf:
            image = Image.open(buf).convert("RGB")

        return image

    def load_display_driver(self, packageName, className):
        """helper method to load a concrete display object based on the package and class name"""
        try:
            # load the given driver module
            driver = importlib.import_module(f"{packageName}.{className}")
        except ModuleNotFoundError:
            # hard stop if driver not
            print(f"{packageName}.{className} not found, refer to install instructions")
            exit(2)

        return driver

    def getName(self):
        """ returns package.device name """
        return self.__str__()

    @staticmethod
    def get_supported_devices():
        """ REQUIRED - a list of devices supported by this class, format is {pkgname.devicename}
        :raises NotImplementedError: if not implemented by child class
        """
        raise NotImplementedError

    def _display(self, image):
        """ REQUIRED - actual display code, PIL image given
        :raises NotImplementedError: if not implemented by child class
        """
        raise NotImplementedError

    def prepare(self):
        """ OPTIONAL - run at the top of each update to do required pre-work """
        return True

    def display(self, image):
        """ Called to draw an image on the display, this applies configured effects
        DON'T override this method directly, use _display() in child classes

        :param image: an Image object
        """
        self._display(self.__applyConfig(image))

    def sleep(self):
        """ OPTIONAL - put the display to sleep after each update, if device supports """
        return True

    def clear(self):
        """ OPTIONAL - clear the display, if device supports """
        return True

    def close(self):
        """ OPTIONAL close out the device, called when the program ends """
        return True
