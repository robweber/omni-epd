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


class InvalidDisplayModeError(Exception):
    """
    InvalidDisplayModeError is thrown when a display mode for a given sign does not match
    the configured allowed display modes
    """

    def __init__(self, deviceName, mode):
        super().__init__(f"'{mode}' is not a valid display mode for {deviceName}")


class TooManyColorsError(Exception):
    """
    TooManyColors is thrown when a the user defined palette for a display has too many colors
    """

    def __init__(self, deviceName, maxColors, givenColors):
        super().__init__(f"{givenColors} colors is too many for {deviceName}, {maxColors} colors supported")
