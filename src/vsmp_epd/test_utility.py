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

import argparse
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

    def __draw_rectangle(self, imgObj, width, height, x, y, percent, step):
        # draw recursively until we go below 0
        if(percent > 0):
            # calculate the dimensions of the rectangle
            rWidth = width * percent
            rHeight = height * percent

            # calculate the starting position to center it
            rX = x + (width - rWidth)/2
            rY = y + (height - rHeight)/2

            print(f"Drawing rectangle of width {rWidth} and height {rHeight}")
            imgObj.rectangle((rX, rY, rWidth + rX, rHeight + rY), width=2)

            return self.__draw_rectangle(imgObj, rWidth, rHeight, rX, rY, percent-step, step)
        else:
            return imgObj

    def isReady(self):
        return self.epd is not None

    def draw(self):

        # create a blank image
        im = Image.new('1', (self.epd.width, self.epd.height), color=1)
        draw = ImageDraw.Draw(im)

        # draw a series of rectangles
        draw = self.__draw_rectangle(draw, self.epd.width, self.epd.height, 0, 0, .75, .25)

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

def main():

    # get the name of the epd driver to use
    parser = argparse.ArgumentParser(description='EPD Test Utility')
    parser.add_argument('-e', '--epd', required=True,
                        help="The type of EPD driver to test")

    args = parser.parse_args()

    test = EPDTestUtility(args.epd)

    if(test.isReady()):
        # this will draw a rectangle in the center of the display
        test.draw()
