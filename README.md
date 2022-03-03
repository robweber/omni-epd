# Omni-EPD
[![build-status](https://img.shields.io/github/workflow/status/robweber/omni-epd/Unit%20Test%20Check?logo=Github)](https://github.com/robweber/omni-epd/actions/workflows/pytest.yml?query=branch%3Amain)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)

An EPD (electronic paper display) class abstraction to simplify communications across multiple display types.

There are several great EPD projects all over the internet, many in written in Python. The problem with a lot of these is that the code is often for one specific type of display, or perhaps a family of displays. This project abstracts the EPD communications into a common interface so a variety of displays can be interchangeably used in the same project.

For project maintainers this expands the number of displays you can use for your project without having to code around each one. To utilize this in your project read the usage instructions. For a list of (known) projects that use this abstraction see the list below.

## Table Of Contents

- [Install](#install)
- [Usage](#usage)
  - [VirtualEPD Object](#virtualepd-object)
  - [Display Testing](#display-testing)
  - [Advanced EPD Control](#advanced-epd-control)
- [Displays Implemented](#displays-implemented)
  - [Display Driver Installation](#display-driver-installation)
- [Implementing Projects](#implementing-projects)
- [Contributing](#contributing)
  - [Contributors](#contributors)
- [License](#license)

## Install

Installing this module installs any required _Python_ library files. Refer to instructions for your specific display for any [additional requirements](#display-driver-installation) that may need to be satisfied. A common requirement is [enabling SPI support](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/) on a Raspberry Pi. Install any required libraries or setup files and then run:

```

sudo pip3 install git+https://github.com/robweber/omni-epd.git#egg=omni-epd

```

This will install the abstraction library. The [test utility](#display-testing) can be used to test your display and ensure everything is working properly. You can also clone this repo and install from source with:

```

git clone https://github.com/robweber/omni-epd.git
cd omni-epd
sudo pip3 install --prefer-binary .

```

## Usage

Usage in this case refers to EPD project implementers that wish to abstract their code with this library. In general, this is pretty simple. This library is meant to be very close to a 1:1 replacement for existing EPD code you may have in your project. Function names may vary slightly but most calls are very similar. Refer to the [examples folder](https://github.com/robweber/omni-epd/tree/main/examples) for some working code examples you can run. In general, once the `VirtualEPD` object is loaded it can interact with your display using the methods described below. For testing, the device `omni_epd.mock` can be used to write output to a JPEG file instead of to a display.

### VirtualEPD Object

Objects returned by the `displayfactory` class all inherit methods from the `VirtualEPD` class. The following methods are available to be implemented once the object is loaded. Be aware that not all displays may implement all methods but `display` is required.

* `width` and `height` - these are convience attributes to get the width and height of the display in your code. See the above example for their use.
* `prepare()` - does any initializing information on the display. This is waking up from sleep or doing anything else prior to a new image being drawn.
* `display(image)` - draws an image on the display. The image must be a [Pillow Image](https://pillow.readthedocs.io/en/stable/reference/Image.html) object.
* `sleep()` - puts the display into sleep mode, if available for that device. Generally this is lower power consumption and maintains better life of the display.
* `clear()` - clears the display
* `close()` - performs any cleanup operations and closes access to the display. Use at the end of a program or when the object is no longer needed.

If the display you're implementing supports any advanced features, like multiple colors, these can be handled by setting some additional variables. Specifically you can set the variables below in the `__init()__` method. See currently implemented displays for a better idea of how to handle multiple colors.

* `modes_available` - a tuple containing the names of valid modes, BW available by default
* `max_colors` - The maximum number of colors supported (up to 256 RGB)
* `palette_filter` - a tuple of RGB values for valid colors an `Image` can send to the display

### Display Testing

There is a utility, `omni-epd-test` to verify the display. This is useful to provide users with a way their hardware is working properly. Many displays have specific library requirements that need to be installed with OS level package utilities and may throw errors until they are resolved. The test utility helps confirm all requirements are met before doing more advanced work with the display. This can be run from the command line, specifying the device from the table below.

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
dither=floyd-steinberg  # apply a dithering algorithm to the image, valid options list below
order=8  # when using bayer and yiluoma dithers defines the matrix size, must be a power of 2. When using cluster-dot dither this defines the dot size, can be 4 or 8
threshold=[128, 128, 128]  # for dithers this defines the color snap threshold. Takes an RGB list.

[Image Enhancements]
palette_filter=[[R,G,B], [R,G,B]]  # for multi color displays the palette filter used to determine colors passed to the display, must be less than or equal to max colors the display supports
contrast=1  # adjust image contrast, 1 = no adjustment
brightness=1  # adjust image brightness, 1 = no adjustment
sharpness=1  # adjust image sharpness, 1 = no adjustment
```

When using the `dither` option the following values are allowed. Be aware that some dithering algorithms take a lot of time to run on smaller systems, like a Raspberry Pi. [Click here](https://tannerhelland.com/2012/12/28/dithering-eleven-algorithms-source-code.html) for more information on dithering, and it's effects.

* floyd-steinberg
* jarvis-judice-ninke
* stucki
* burkes
* sierra3
* sierra2
* sierra-2-4a
* atkinson
* bayer
* cluster-dot
* yliluoma

## Displays Implemented
Below is a list of displays currently implemented in the library. The Omni Device Name is what you'd pass to `displaymanager.load_display_driver(deviceName)` to load the correct device driver. Generally this is the `packagename.devicename` Devices in __bold__ have been tested on actual hardware while others have been implemented but not verified. This often happens when multiple displays use the same libraries but no physical verification has happened for all models. The color modes are available modes that can be set on the device.

| Device Library | Device Name | Omni Device Name | Color Modes |
|:---------------|:------------|:-----------------|-------------|
| [Inky](https://github.com/pimoroni/inky) | [Inky Impression 7 Color](https://shop.pimoroni.com/products/inky-impression) | __inky.impression__ | bw, color |
| | [Inky pHAT Red/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811) - 212x104 | __inky.phat_red__ | bw, red |
| | [Inky pHAT Yellow/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254905939) - 212x104 | inky.phat_yellow | bw, yellow |
| | [Inky pHAT Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254938707) - 212x104 | inky.phat_black | bw |
| | [Inky pHAT Red/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811) - 250x122 | inky.phat1608_red | bw, red |
| | [Inky pHAT Yellow/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254905939) - 250x122 | inky.phat1608_yellow | bw, yellow |
| | [Inky pHAT Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254938707) - 250x122 | inky.phat1608_black | bw |
| | [Inky wHAT Red/Black/White](https://shop.pimoroni.com/products/inky-what?variant=13590497624147) | inky.what_red | bw, red |
| | [Inky wHAT Yellow/Black/White](https://shop.pimoroni.com/products/inky-what?variant=21441988558931) | inky.what_yellow | bw, yellow |
| | [Inky wHAT Black/White](https://shop.pimoroni.com/products/inky-what?variant=21214020436051) | inky.what_black | bw |
| | [Inky wHAT AutoDetect](https://shop.pimoroni.com/search?q=inky) | inky.auto | black, yellow, red, colour |
| Omni-EPD | Mock Display (emulates EPD with no hardware) | __omni_epd.mock__ | bw, color, palette |
| [Waveshare](https://github.com/waveshare/e-Paper) | [1.02inch E-Ink display module](https://www.waveshare.com/1.02inch-e-Paper-Module.htm) | waveshare_epd.epdlin02 | bw |
|  | [1.54inch E-Ink display module](https://www.waveshare.com/1.54inch-e-Paper-Module.htm) | waveshare_epd.epdlin54 <br> waveshare_epd.epdlin54_V2 | bw |
|  | [1.54inch e-Paper Module B](https://www.waveshare.com/1.54inch-e-Paper-Module-B.htm) | waveshare_epd.epdlin54b <br> waveshare_epd.epdlin54b_V2 | bw, red |
|  | [1.54inch e-Paper Module C ](https://www.waveshare.com/1.54inch-e-Paper-Module-C.htm) | waveshare_epd.epdlin54c | bw, yellow |
|  | [2.13inch e-Paper HAT](https://www.waveshare.com/2.13inch-e-Paper-HAT.htm) | waveshare_epd.epd2in13 <br>  waveshare_epd.epd2in13_V2 | bw |
|  | [2.13inch e-Paper HAT B](https://www.waveshare.com/2.13inch-e-Paper-HAT-B.htm) | waveshare_epd.epd2in13b <br> waveshare_epd.epd2in13b_V3 | bw, red |
|  | [2.13inch e-Paper HAT C ](https://www.waveshare.com/2.13inch-e-Paper-HAT-C.htm) | waveshare_epd.epd2in13c | bw, yellow |
|  | [2.13inch e-Paper HAT D](https://www.waveshare.com/2.13inch-e-Paper-HAT-D.htm) | waveshare_epd.epd2in13d | bw |
|  | [2.66inch e-Paper Module](https://www.waveshare.com/2.66inch-e-Paper-Module.htm) | waveshare_epd.epd2in66 | bw |
|  | [2.66inch e-Paper Module B](https://www.waveshare.com/2.66inch-e-Paper-Module-B.htm) | waveshare_epd.epd2in66b | bw, red |
|  | [2.7inch e-Paper HAT](https://www.waveshare.com/2.7inch-e-Paper-HAT.htm) | __waveshare_epd.epd2in7__ | bw |
|  | [2.7inch e-Paper HAT B](https://www.waveshare.com/2.7inch-e-Paper-HAT-B.htm) | waveshare_epd.epd2in7b <br> waveshare_epd.epd2in7b_V2 | bw, red |
|  | [2.9inch e-Paper Module](https://www.waveshare.com/2.9inch-e-Paper-Module.htm) | __waveshare_epd.epd2in9__ <br> waveshare_epd.epd2in9_V2 | bw |
|  | [2.9inch e-Paper Module B](https://www.waveshare.com/2.9inch-e-Paper-Module-B.htm) | waveshare_epd.epd2in9b <br> waveshare_epd.epd2in9b_V3 | bw, red |
|  | [2.9inch e-Paper Module C](https://www.waveshare.com/2.9inch-e-Paper-Module-C.htm) | waveshare_epd.epd2in9c | bw, yellow |
|  | [2.9inch e-Paper HAT D](https://www.waveshare.com/2.9inch-e-Paper-HAT-D.htm) | waveshare_epd.epd2in9d | bw |
|  | [3.7inch e-Paper HAT](https://www.waveshare.com/3.7inch-e-Paper-HAT.htm) | __waveshare_epd.epd3in7__ | gray4 |
|  | [4.01inch 7 color e-Paper HAT](https://www.waveshare.com/4.01inch-e-paper-hat-f.htm) | waveshare_epd.epd4in01f | bw, color |
|  | [4.2inch e-Paper Module](https://www.waveshare.com/4.2inch-e-Paper-Module.htm) |waveshare_epd.epd4in2 | bw |
|  | [4.2inch e-Paper Module B](https://www.waveshare.com/4.2inch-e-Paper-Module-B.htm) |waveshare_epd.epd4in2b <br> waveshare_epd.epd4in2b_V2 | bw, red |
|  | [4.2inch e-Paper Module C](https://www.waveshare.com/4.2inch-e-Paper-Module-C.htm) |waveshare_epd.epd4in2c | bw, yellow |
|  | [5.65inch e-Paper Module F](https://www.waveshare.com/5.65inch-e-Paper-Module-F.htm) |__waveshare_epd.epd5in65f__ | bw, color |
|  | [5.83inch e-Paper HAT](https://www.waveshare.com/5.83inch-e-Paper-HAT.htm) |waveshare_epd.epd5in83 <br> waveshare_epd.epd5in83_V2 | bw |
|  | [5.83inch e-Paper HAT B](https://www.waveshare.com/5.83inch-e-Paper-HAT-B.htm) |waveshare_epd.epd5in83b <br> waveshare_epd.epd5in83b_V2 | bw, red |
|  | [5.83inch e-Paper HAT C](https://www.waveshare.com/5.83inch-e-Paper-HAT-C.htm) | __waveshare_epd.epd5in83c__ | bw, yellow |
|  | [7.5inch e-Paper HAT](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm) | waveshare_epd.epd7in5 | bw |
|  | [7.5inch e-Paper HAT V2](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm) | __waveshare_epd.epd7in5_V2__ | bw |
|  | [7.5inch HD e-Paper HAT](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT.htm) |waveshare_epd.epd7in5_HD | bw |
|  | [7.5inch HD e-Paper HAT B](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT-B.htm) |waveshare_epd.epd7in5b_HD | bw, red |
|  | [7.5inch e-Paper HAT B](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT-B.htm)| waveshare_epd.epd7in5b | bw, red |
|  | [7.5inch e-Paper HAT B V2](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT-B.htm)| __waveshare_epd.epd7in5b_V2__ | bw, red |
|  | [7.5inch e-Paper HAT C](https://www.waveshare.com/7.5inch-e-Paper-HAT-C.htm) | waveshare_epd.epd7in5c | bw, yellow |


### Display Driver Installation

Each display type has different install requirements depending on the platform.  While loading this module will install any required _Python_ libraries for supported displays; specific OS level configuration may need to be done. Basic instructions are below for each library type. Refer to instructions for your specific display to make sure you've satisfied these requirements. The `omni-epd-test` utility can be used to verify things are working properly.

__Inky__

Inky makes things pretty easy with a one-line installer. This makes the necessary OS level changes and pulls in the [Inky library](https://github.com/pimoroni/inky/).

```
curl https://get.pimoroni.com/inky | bash
```

__Waveshare__

The [Waveshare device library](https://github.com/waveshare/e-Paper) requires that [SPI support](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/) be enabled on your system prior to use. The `waveshare-epd` module is automatically downloaded and installed as a dependency of this module.  

## Implementing Projects
Below is a list of known projects currently utilizing `omni-epd`. If you're interested in building a very small media player, check them out.

* [SlowMovie](https://github.com/TomWhitwell/SlowMovie) - A very popular VSMP player with lots of options for playing files and an easy install process.
* [VSMP+](https://github.com/robweber/vsmp-plus) - My own VSMP project with a built in web server for easy administration.

## Contributing

PRs accepted! If there a fix for any of the documentation or something is not quite clear, please [point it out](https://github.com/robweber/omni-epd/issues). If you test one of the listed displays, please mark it as verified by __bolding__ it in the [Displays Implemented](#displays-implemented) section. If you want to extend this framework by adding a new display type; a good place to start is one of the [existing display classes](https://github.com/robweber/omni-epd/tree/main/src/omni_epd/displays) for an example.

### Contributors

* [@missionfloyd](https://github.com/missionfloyd)
* [@qubist](https://github.com/qubist)
* [@dr-boehmerie](https://github.com/dr-boehmerie)
* [@aaronr8684](https://github.com/aaronr8684)
* [@donbing](https://github.com/donbing)

## License
[GPLv3](/LICENSE)
