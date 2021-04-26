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

import configparser
import importlib
import os
import logging
from . errors import EPDNotFoundError, EPDConfigurationError
from . conf import CONFIG_FILE, EPD_CONFIG
from . virtualepd import VirtualEPD
from . displays.mock_display import MockDisplay  # noqa: F401
from . displays.waveshare_display import WaveshareDisplay, WaveshareTriColorDisplay, Waveshare102inDisplay, WaveshareGrayscaleDisplay, Waveshare565finDisplay  # noqa: F401,E501
from . displays.inky_display import InkyDisplay, InkyImpressionDisplay  # noqa: F401


def __loadConfig(deviceName):
    logger = logging.getLogger(__name__)

    config = configparser.ConfigParser()

    # check for global ini file
    if(os.path.exists(os.path.join(os.getcwd(), CONFIG_FILE))):
        config.read(os.path.join(os.getcwd(), CONFIG_FILE))
        logger.debug(f"Loading {CONFIG_FILE}")

    # possible device name exists in global configuration file
    if(not deviceName and config.has_option(EPD_CONFIG, 'type')):
        deviceName = config.get(EPD_CONFIG, 'type')

    # check for device specific ini file
    if(deviceName and os.path.exists(os.path.join(os.getcwd(), f"{deviceName}.ini"))):
        config.read(os.path.join(os.getcwd(), f"{deviceName}.ini"))
        logger.debug(f"Loading {deviceName}.ini")

    return config


def list_supported_displays(as_dict=False):
    result = []

    # get a list of display classes extending VirtualDisplayDevice
    displayClasses = [(cls.__module__, cls.__name__) for cls in VirtualEPD.__subclasses__()]

    for modName, className in displayClasses:
        # load the module the class belongs to
        mod = importlib.import_module(modName)
        # get the class
        classObj = getattr(mod, className)

        if(as_dict):
            result.append({'package': modName, 'class': className, 'devices': classObj.get_supported_devices()})
        else:
            # add supported devices of this class
            result = sorted(result + classObj.get_supported_devices())

    return result


def load_display_driver(displayName='', configDict={}):
    result = None

    # load any config files and merge passed in configs
    config = __loadConfig(displayName)
    config.read_dict(configDict)

    # possible device name is part of global conf
    if(not displayName and config.has_option(EPD_CONFIG, 'type')):
        displayName = config.get(EPD_CONFIG, 'type')

    # get a dict of all valid display device classes
    displayClasses = list_supported_displays(True)
    foundClass = list(filter(lambda d: displayName in d['devices'], displayClasses))

    if(len(foundClass) == 1):
        # split on the pkg.classname
        deviceType = displayName.split('.')

        # create the class and initialize
        mod = importlib.import_module(foundClass[0]['package'])
        classObj = getattr(mod, foundClass[0]['class'])

        result = classObj(deviceType[1], config)

        # check that the display mode is valid - must be done after class loaded
        if(result.mode not in result.modes_available):
            raise EPDConfigurationError(displayName, "mode", result.mode)

    else:
        # we have a problem
        raise EPDNotFoundError(displayName)

    return result
