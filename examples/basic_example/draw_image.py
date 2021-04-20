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
from vsmp_epd import displayfactory, EPDNotFoundError
from PIL import Image

"""
This basic example will load your device (modify string below),
load an image, and then write it to the display

"""
# load your particular display using the displayfactory
displayName = "vsmp_epd.mock"

print('Loading display')
try:
    epd = displayfactory.load_display_driver(displayName)
except EPDNotFoundError:
    print(f"Couldn't find {displayName}")
    sys.exit()

 # if now load an image file using the Pillow lib
print('Loading image')
image = Image.open('../grass.jpg')

# resize for your display
image = image.resize((epd.width, epd.height))

 # prepare the epd, write the image, and close
print('Writing to display')
epd.prepare()

epd.display(image)

epd.close()
