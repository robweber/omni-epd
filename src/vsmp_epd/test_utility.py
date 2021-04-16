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

from . import displayfactory
from PIL import Image, ImageDraw


class EPDTestUtility:
    """
    A simple test utility to make sure all display pre-reqs are met.
    Can test draw and clear capabilities for a given display
    """
    epd = None

    def __init__(self, displayName):

        validDisplays = displayfactory.list_supported_displays()

        if(displayName in validDisplays):
            self.epd = displayfactory.load_display_driver(displayName)

            print(f"Loaded {self.epd} with width {self.epd.width} and height {self.epd.height}")
        else:
            print(f"{displayName} is not a valid display. Valid options are:")
            print("\n".join(map(str, validDisplays)))

    def isReady(self):
        return self.epd is not None

    def draw(self):

        # create a blank image
        im = Image.new('1', (self.epd.width, self.epd.height), color=1)
        draw = ImageDraw.Draw(im)

        # rectangle will be width * 3 and height * 3
        rWidth = self.epd.width/4
        rHeight = self.epd.height/4

        print(f"Drawing rectangle of width {rWidth * 3} and height {rHeight * 3}")
        draw.rectangle((rWidth, rHeight, rWidth * 3, rHeight * 3), width=3)

        self.epd.prepare()

        self.epd.display(im)

        self.epd.close()

        print("Display closed - testing complete")

    def clear(self):
        print("Clearing display")
        self.epd.prepare()

        self.epd.clear()

        self.epd.close()

        print("Display closed - testing complete")
