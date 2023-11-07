# Omni-EPD
[![build-status](https://img.shields.io/github/actions/workflow/status/robweber/omni-epd/pytest.yml?branch=main)](https://github.com/robweber/omni-epd/actions/workflows/pytest.yml?query=branch%3Amain)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)

An EPD (electronic paper display) class abstraction to simplify communications across multiple display types.

There are several great EPD projects all over the internet, many in written in Python. The problem with a lot of these is that the code is often for one specific type of display, or perhaps a family of displays. This project abstracts the EPD communications into a common interface so a variety of displays can be interchangeably used in the same project. It also adds a lot of [helpful conveniences](#advanced-epd-control) such as the ability to automatically to rotate, add contrast, or dither images on their way to the display. This gives more control to end users without having to add extra features in your upstream project.

For EPD project builders this expands the number of displays you can use for your project without having to code around each one. To utilize this in your project read the usage instructions. For a list of (known) projects that use this abstraction see the [list below](#displays-implmented).

## Table Of Contents

- [Install](#install)
  - [Python Virtual Environments](#python-virtual-environments)
- [Usage](#usage)
  - [VirtualEPD Object](#virtualepd-object)
  - [Display Testing](#display-testing)
  - [Advanced EPD Control](#advanced-epd-control)
  - [Dithering](#dithering)
- [Displays Implemented](#displays-implemented)
  - [Display Driver Installation](#display-driver-installation)
- [Implementing Projects](#implementing-projects)
- [Acknowledgements](#acknowledgements)
- [Contributing](#contributing)
  - [Contributors](#contributors)
- [License](#license)

## Install

Installing this module installs any required _Python_ library files. Refer to instructions for your specific display for any [additional requirements](#display-driver-installation) that may need to be satisfied. A common requirement is [enabling SPI support](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/) on a Raspberry Pi. Install any required libraries or setup files and then run:

```

pip3 install git+https://github.com/robweber/omni-epd.git#egg=omni-epd

```

This will install the abstraction library. The [test utility](#display-testing) can be used to test your display and ensure everything is working properly. You can also clone this repo and install from source with:

```

git clone https://github.com/robweber/omni-epd.git
cd omni-epd
pip3 install --prefer-binary .

```

### Python Virtual Environments

It is best practice to install inside a [virtual environment]( http://rptl.io/venv). For implementing projects you may experience errors installing outside of a virtual environment.

The [numpy](https://numpy.org/) package, required by Pillow, needs access to the system installed version of _numpy_ in order to work properly. When setting up your virtual environment be sure to pass in the `--system-site-packages` argument to enable using system packages if they're available. An example would be:

```
# create the environment
python3 -m venv --system-site-packages .venv

# activate the environment
source .venv/bin/activate

# deactivate the environment
deactivate
```

## Usage

Usage in this case refers to EPD project implementers that wish to abstract their code with this library. In general, this is pretty simple. This library is meant to be very close to a 1:1 replacement for existing EPD code you may have in your project. Function names may vary slightly but most calls are very similar. Refer to the [examples folder](https://github.com/robweber/omni-epd/tree/main/examples) for some working code examples you can run. In general, once the `VirtualEPD` object is loaded it can interact with your display using the methods described below. For testing, the device `omni_epd.mock` can be used to write output to a PNG file instead of to a display.

### VirtualEPD Object

Objects returned by the `displayfactory` class all inherit methods from the `VirtualEPD` class. The following methods are available to be implemented once the object is loaded. Be aware that not all displays may implement all methods but `display` is required.

* `width` and `height` - these are convenience attributes to get the width and height of the display in your code.
* `prepare()` - does any initializing information on the display. This is waking up from sleep or doing anything else prior to a new image being drawn.
* `display(image)` - draws an image on the display. The image must be a [Pillow Image](https://pillow.readthedocs.io/en/stable/reference/Image.html) object.
* `sleep()` - puts the display into sleep mode, if available for that device. Generally this is lower power consumption and maintains longer life of the display.
* `clear()` - clears the display
* `close()` - performs any cleanup operations and closes access to the display. Use at the end of a program or when the object is no longer needed.

If the display you're using supports any advanced features, like multiple colors, these can be handled by setting some additional variables. See [advanced display control](#advanced-epd-control) for a better idea of how to additional options.

* `modes_available` - a tuple containing the names of valid modes, __BW__ available by default
* `max_colors` - The maximum number of colors supported (up to 256 RGB)
* `palette_filter` - a tuple of RGB values for valid colors an `Image` can send to the display

### Display Testing

There is a utility, `omni-epd-test` to verify the display. This is useful to provide users with a way to test that their hardware is working properly. Many displays have specific library requirements that need to be installed with OS level package utilities and may throw errors until they are resolved. The test utility helps confirm all requirements are met before doing more advanced work with the display. This can be run from the command line, specifying the device from the table below.

```
# this will draw a series of rectangles
user@server:~ $ omni-epd-test -e omni_epd.mock

# this will draw the specified image
user@server:~ $ omni-epd-test -e omni_epd.mock -i /path/to/image.jpg

```

### Advanced EPD Control

There are scenarios where additional post-processing needs to be done for a particular project, or a particular display. An example of this might be to rotate the display 180 degrees to account for how the physical hardware is mounted. Another might be always adjusting the image with brightness or contrast settings. These are modifications that are specific to display requirements or user preferences and can be applied by use of a .ini file instead of having to modify code or allow for options via implementing scripts.

Two types of __ini__ files can be used in these situations. A global file, named `omni-epd.ini`, or a device specific file; which is the device name from the table below with a `.ini` suffix. These must exist in the root directory where the calling script is run. This is the directory given by the `os.getcwd()` method call. Valid options for this file are listed below. These will be applied on top of any processing done to the passed in image object. For example, if the implementing script is already modifying the image object to rotate 90 degrees, adding a rotate command will rotate an additional X degrees. For precedence device specific configurations trump any global configurations. Some displays also have options specific to them only. [Consult with that list](https://github.com/robweber/omni-epd/wiki/Device-Specific-Options) if these additional options are needed in your situation.

```
# file shown with default values
[EPD]
type=none  # only valid in the global configuration file, will load this display if none given to displayfactor.load_display_driver()
mode=bw  # the mode of the display, typically b+w by default. See list of supported modes for each display below

[Display]
rotate=0  # rotate final image written to display by X degrees [0-360]
flip_horizontal=False  # flip image horizontally
flip_vertical=False  # flip image vertically
dither=FloydSteinberg  # apply a dithering algorithm to the image

[Image Enhancements]
palette_filter=[[R,G,B], [R,G,B]]  # for multi color displays the palette filter used to determine colors passed to the display, must be less than or equal to max colors the display supports
contrast=1  # adjust image contrast, 1 = no adjustment
brightness=1  # adjust image brightness, 1 = no adjustment
sharpness=1  # adjust image sharpness, 1 = no adjustment
```

__Palette Filtering__

The `palette_filter` option controls what colors are passed to multi color displays by filtering the image so only the listed colors remain. The total number of colors must be less than or equal to the max number of colors the display supports. Colors can be specified as an array of RGB values (`[[R,G,B], [R,G,B]]`), hexidecimal values (`#ff0000, #00ff00`), or [color names](https://github.com/python-pillow/Pillow/blob/e3cb4bb8e00fcaf4c3e0783f7c02e51372595659/src/PIL/ImageColor.py#L153-L305) (`blue, maroon`). Combinations of these can also be given as long as each color specified is separated by a comma.

### Dithering

When using the `dither` option many algorithms are available. Please read the [full instructions](https://github.com/robweber/omni-epd/wiki/Image-Dithering-Options) for dithering and how it can be used.

## Displays Implemented
Below is a list of displays currently implemented in the library. The Omni Device Name is what you'd pass to `displaymanager.load_display_driver(deviceName)` to load the correct device driver. Generally this is the `packagename.devicename` Devices in __bold__ have been tested on actual hardware while others have been implemented but not verified. This often happens when multiple displays use the same libraries but no physical verification has happened for all models. The color modes are available modes that can be set on the device.

| Device Library | Device Name | Omni Device Name | Color Modes |
|:---------------|:------------|:-----------------|-------------|
| [Inky](https://github.com/pimoroni/inky) | [Inky AutoDetect](https://shop.pimoroni.com/search?q=inky) | inky.auto | bw, yellow, red, color |
| | [Inky Impression 7 Color](https://shop.pimoroni.com/products/inky-impression) | __inky.impression__ | bw, color |
| | [Inky pHAT Red/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811) - 212x104 | __inky.phat_red__ | bw, red |
| | [Inky pHAT Yellow/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254905939) - 212x104 | inky.phat_yellow | bw, yellow |
| | [Inky pHAT Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254938707) - 212x104 | inky.phat_black | bw |
| | [Inky pHAT Red/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811) - 250x122 | inky.phat1608_red | bw, red |
| | [Inky pHAT Yellow/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254905939) - 250x122 | inky.phat1608_yellow | bw, yellow |
| | [Inky pHAT Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254938707) - 250x122 | inky.phat1608_black | bw |
| | [Inky wHAT Red/Black/White](https://shop.pimoroni.com/products/inky-what?variant=13590497624147) | __inky.what_red__ | bw, red |
| | [Inky wHAT Yellow/Black/White](https://shop.pimoroni.com/products/inky-what?variant=21441988558931) | inky.what_yellow | bw, yellow |
| | [Inky wHAT Black/White](https://shop.pimoroni.com/products/inky-what?variant=21214020436051) | inky.what_black | bw |
| Omni-EPD | Mock Display (emulates EPD with no hardware) | __omni_epd.mock__ | bw, color, palette |
| [Waveshare](https://github.com/waveshareteam/e-Paper) | [1.02inch E-Ink display module](https://www.waveshare.com/1.02inch-e-Paper-Module.htm) | waveshare_epd.epdlin02 | bw |
|  | [1.54inch E-Ink display module](https://www.waveshare.com/1.54inch-e-Paper-Module.htm) | waveshare_epd.epdlin54 <br> waveshare_epd.epdlin54_V2 | bw |
|  | [1.54inch e-Paper Module B](https://www.waveshare.com/1.54inch-e-Paper-Module-B.htm) | waveshare_epd.epdlin54b <br> waveshare_epd.epdlin54b_V2 | bw, red |
|  | [1.54inch e-Paper Module C ](https://www.waveshare.com/1.54inch-e-Paper-Module-C.htm) | waveshare_epd.epdlin54c | bw, yellow |
|  | [1.64inch e-Paper Module G ](https://www.waveshare.com/1.64inch-e-paper-module-g.htm) | waveshare_epd.epd1in64g | bw, red, yellow, 4color |
|  | [2.13inch e-Paper HAT](https://www.waveshare.com/2.13inch-e-Paper-HAT.htm) | waveshare_epd.epd2in13 <br>  waveshare_epd.epd2in13_V2 <br> __waveshare_epd.epd2in13_V3__ | bw |
|  | [2.13inch e-Paper HAT B](https://www.waveshare.com/2.13inch-e-Paper-HAT-B.htm) | waveshare_epd.epd2in13b <br> waveshare_epd.epd2in13b_V3 | bw, red |
|  | [2.13inch e-Paper HAT C ](https://www.waveshare.com/2.13inch-e-Paper-HAT-C.htm) | waveshare_epd.epd2in13c | bw, yellow |
|  | [2.13inch e-Paper HAT D](https://www.waveshare.com/2.13inch-e-Paper-HAT-D.htm) | waveshare_epd.epd2in13d | bw |
|  | [2.36inch e-Paper Module G](https://www.waveshare.com/2.36inch-e-paper-module-g.htm) | waveshare_epd.epd2in36g | bw, red, yellow, 4color |
|  | [2.66inch e-Paper Module](https://www.waveshare.com/2.66inch-e-Paper-Module.htm) | waveshare_epd.epd2in66 | bw |
|  | [2.66inch e-Paper Module B](https://www.waveshare.com/2.66inch-e-Paper-Module-B.htm) | waveshare_epd.epd2in66b | bw, red |
|  | [2.7inch e-Paper HAT](https://www.waveshare.com/2.7inch-e-Paper-HAT.htm) | __waveshare_epd.epd2in7__ | bw |
|  | [2.7inch e-Paper HAT B](https://www.waveshare.com/2.7inch-e-Paper-HAT-B.htm) | waveshare_epd.epd2in7b <br> __waveshare_epd.epd2in7b_V2__ | bw, red |
|  | [2.9inch e-Paper Module](https://www.waveshare.com/2.9inch-e-Paper-Module.htm) | __waveshare_epd.epd2in9__ <br> waveshare_epd.epd2in9_V2 | bw |
|  | [2.9inch e-Paper Module B](https://www.waveshare.com/2.9inch-e-Paper-Module-B.htm) | waveshare_epd.epd2in9b <br> waveshare_epd.epd2in9b_V3 | bw, red |
|  | [2.9inch e-Paper Module C](https://www.waveshare.com/2.9inch-e-Paper-Module-C.htm) | waveshare_epd.epd2in9c | bw, yellow |
|  | [2.9inch e-Paper HAT D](https://www.waveshare.com/2.9inch-e-Paper-HAT-D.htm) | waveshare_epd.epd2in9d | bw |
|  | [3inch e-Paper Module G](https://www.waveshare.com/3inch-e-paper-module-g.htm) | __waveshare_epd.epd3in0g__ | bw, red, yellow, 4color |
|  | [3.7inch e-Paper HAT](https://www.waveshare.com/3.7inch-e-Paper-HAT.htm) | __waveshare_epd.epd3in7__ | gray4 |
|  | [4.01inch 7 color e-Paper HAT](https://www.waveshare.com/4.01inch-e-paper-hat-f.htm) | waveshare_epd.epd4in01f | bw, color |
|  | [4.2inch e-Paper Module](https://www.waveshare.com/4.2inch-e-Paper-Module.htm) |waveshare_epd.epd4in2 | bw |
|  | [4.2inch e-Paper Module B](https://www.waveshare.com/4.2inch-e-Paper-Module-B.htm) |waveshare_epd.epd4in2b <br> waveshare_epd.epd4in2b_V2 | bw, red |
|  | [4.2inch e-Paper Module C](https://www.waveshare.com/4.2inch-e-Paper-Module-C.htm) | __waveshare_epd.epd4in2c__ | bw, yellow |
|  | [4.37inch e-Paper Module G](https://www.waveshare.com/4.37inch-e-paper-module-g.htm) | waveshare_epd.epd4in37g | bw, red, yellow, 4color |
|  | [5.65inch e-Paper Module F](https://www.waveshare.com/5.65inch-e-Paper-Module-F.htm) |__waveshare_epd.epd5in65f__ | bw, color |
|  | [5.83inch e-Paper HAT](https://www.waveshare.com/5.83inch-e-Paper-HAT.htm) |waveshare_epd.epd5in83 <br> waveshare_epd.epd5in83_V2 | bw |
|  | [5.83inch e-Paper HAT B](https://www.waveshare.com/5.83inch-e-Paper-HAT-B.htm) |waveshare_epd.epd5in83b <br> waveshare_epd.epd5in83b_V2 | bw, red |
|  | [5.83inch e-Paper HAT C](https://www.waveshare.com/5.83inch-e-Paper-HAT-C.htm) | __waveshare_epd.epd5in83c__ | bw, yellow |
|  | [6inch e-Ink Display](https://www.waveshare.com/6inch-e-paper-hat.htm) | waveshare_epd.it8951 | bw, gray16 |
|  | [7.3inch e-Paper HAT G](https://www.waveshare.com/7.3inch-e-paper-hat-g.htm) | waveshare_epd.epd7in3g | bw, red, yellow, 4color |
|  | [7.3inch e-Paper HAT F](https://www.waveshare.com/7.3inch-e-paper-hat-f.htm) | waveshare_epd.epd7in3f | bw, color |
|  | [7.5inch e-Paper HAT](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm) | waveshare_epd.epd7in5 | bw |
|  | [7.5inch e-Paper HAT V2](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm) | __waveshare_epd.epd7in5_V2__ | bw |
|  | [7.5inch HD e-Paper HAT](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT.htm) |waveshare_epd.epd7in5_HD | bw |
|  | [7.5inch HD e-Paper HAT B](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT-B.htm) |waveshare_epd.epd7in5b_HD | bw, red |
|  | [7.5inch e-Paper HAT B](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT-B.htm)| waveshare_epd.epd7in5b | bw, red |
|  | [7.5inch e-Paper HAT B V2](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT-B.htm)| __waveshare_epd.epd7in5b_V2__ | bw, red |
|  | [7.5inch e-Paper HAT C](https://www.waveshare.com/7.5inch-e-Paper-HAT-C.htm) | waveshare_epd.epd7in5c | bw, yellow |
|  | [7.8inch e-Ink Display](https://www.waveshare.com/7.8inch-e-paper-hat.htm) | waveshare_epd.it8951 | bw, gray16 |
|  | [9.7inch e-Ink Display](https://www.waveshare.com/9.7inch-e-paper-hat.htm) | waveshare_epd.it8951 | bw, gray16 |
|  | [10.3inch e-Ink Display](https://www.waveshare.com/10.3inch-e-paper-hat.htm) | __waveshare_epd.it8951__ | bw, gray16 |

### Display Driver Installation

Each display type has different install requirements depending on the platform.  While loading this module will install any required _Python_ libraries for supported displays; specific OS level configuration may need to be done. Basic instructions are below for each library type. Refer to instructions for your specific display to make sure you've satisfied these requirements. The `omni-epd-test` utility can be used to verify things are working properly.

__Inky__

Inky makes things pretty easy with a one-line installer. This makes the necessary OS level changes and pulls in the [Inky library](https://github.com/pimoroni/inky/).

```
curl https://get.pimoroni.com/inky | bash
```

If installing Inky manually be sure that SPI and I2C are enabled via `sudo raspi-config`.

__Waveshare__

The [Waveshare device library](https://github.com/waveshareteam/e-Paper) requires that [SPI support](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/) be enabled on your system prior to use. The `waveshare-epd` module is automatically downloaded and installed as a dependency of this module.  

__IT8951__

IT8951 devices, such as the [Waveshare 6in EPD](https://www.waveshare.com/6inch-e-paper-hat.htm), are supported via a [separately maintained Python module](https://github.com/GregDMeyer/IT8951) from Greg Kahanamoku-Meyer. This module and it's requirements are downloaded as part of omni-epd setup.

## Implementing Projects
Below is a list of known projects currently utilizing `omni-epd`. If you're interested in building a very small media player, check them out.

* [SlowMovie](https://github.com/TomWhitwell/SlowMovie) - A very popular VSMP player with lots of options for playing files and an easy install process.
* [VSMP+](https://github.com/robweber/vsmp-plus) - My own VSMP project with a built in web server for easy administration.
* [pycasso](https://github.com/jezs00/pycasso) - System to send AI generated art to an E-Paper display through a Raspberry PI unit.

## Acknowledgements

Dithering support provided by the __didder__ Tool - https://github.com/makeworld-the-better-one/didder

## Contributing

PRs accepted! If there a fix for any of the documentation or something is not quite clear, please [point it out](https://github.com/robweber/omni-epd/issues). If you test one of the listed displays, please mark it as verified by __bolding__ it in the [Displays Implemented](#displays-implemented) section. If you want to extend this framework by adding a new display type; a good place to start is one of the [existing display classes](https://github.com/robweber/omni-epd/tree/main/src/omni_epd/displays) for an example.

### Contributors

* [@missionfloyd](https://github.com/missionfloyd)
* [@qubist](https://github.com/qubist)
* [@dr-boehmerie](https://github.com/dr-boehmerie)
* [@aaronr8684](https://github.com/aaronr8684)
* [@donbing](https://github.com/donbing)
* [@evelyndooley](https://github.com/evelyndooley)

## License
[GPLv3](/LICENSE)
