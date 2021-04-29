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
import sys
from omni_epd import displayfactory, EPDNotFoundError
from PIL import Image

"""
This example will load your display from the INI file in this directory.
It will then load the image and write it to the display, applying the image
post-processing rules also defined in the INI file, these are:

* rotate 180 degrees
* apply contrast
* sharpen image

"""
# load your particular display using the displayfactory, driver specified in INI file
print('Loading display')
try:
    epd = displayfactory.load_display_driver()
except EPDNotFoundError:
    print("Couldn't find your display")
    sys.exit()

# if now load an image file using the Pillow lib
print('Loading image')
image = Image.open('../PIA03519_small.jpg')

# resize for your display
image = image.resize((epd.width, epd.height))

# prepare the epd, write the image, and close
print('Writing to display')
print("Rotating image 180 degrees, adjusting sharpness and contrast")
epd.prepare()

epd.display(image)

epd.close()
