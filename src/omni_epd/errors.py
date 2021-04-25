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


class EPDNotFoundError(Exception):
    """
    An EPDNotFoundError is thrown when no display can be loaded for the given device name
    """

    def __init__(self, deviceName):
        super().__init__(f"A display device for device name {deviceName} cannot be loaded")


class EPDConfigurationError(Exception):
    """
    EPDConfigurationError is thrown when an invalid configuration option is given for a display
    this could be an invalid display mode, color option, or other issue
    """

    def __init__(self, deviceName, optionName, optionValue):
        super().__init__(f"'{optionValue}' for '{optionName}' is not a valid configuration value for {deviceName}")
