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

import configparser
import importlib
import os
from . errors import EPDNotFoundError
from . conf import CONFIG_FILE
from . virtualepd import VirtualEPD
from . displays.mock_display import MockDisplay  # noqa: F401
from . displays.waveshare_display import WaveshareDisplay  # noqa: F401


def __loadConfig():
    config = configparser.ConfigParser()

    if(os.path.exists(os.path.join(os.getcwd(), CONFIG_FILE))):
        config.read(os.path.join(os.getcwd(), CONFIG_FILE))

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


def load_display_driver(displayName, configDict={}):
    result = None

    # load any config files and merge passed in configs
    config = __loadConfig()
    config.read_dict(configDict)

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
    else:
        # we have a problem
        raise EPDNotFoundError(displayName)

    return result
