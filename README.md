# VSMP-EPD Abstraction
[![pypi-version](https://img.shields.io/pypi/v/vsmp-epd)](https://pypi.org/project/vsmp-epd/)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)


EPD (electronic paper display) class abstractions for very slow media players

There are several implementations of very slow media players (VSMP), many in Python. The problem with a lot of these is that the code is often for one specific type of display, or perhaps a family of displays. This project abstracts the EPD classes into a common interface so a variety of displays can be interchangeably used in the same project.

For VSMP project maintainers this expands the number of displays you can use for your project without having to code around each one. To utilize this in your VSMP project read the usage instructions. For a list of (known) projects that use this abstraction see the list below.

## Install

Installing this module installs any required _Python_ library files. Refer to instructions for your specific display for any [additional requirements](https://github.com/robweber/vsmp-epd#display-driver-installation) that may need to be satisfied. A common requirement is [enabling SPI support](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/) on a Raspberry Pi. Install any required libraries or setup files and then run:

```

sudo pip3 install vsmp-epd

```

This will install the abstraction library. The [test utility](https://github.com/robweber/vsmp-epd#display-testing) can be used to test your display and ensure everything is working properly.

## Usage

Usage in this case refers to VSMP project implementers that wish to abstract their EPD code with this library. In general, this is pretty simple. This library is meant to be very close to a 1:1 replacement for existing EPD code you may have in your project. Function names may vary slightly but most calls are very similar. Refer to the [examples folder](https://github.com/robweber/vsmp-epd/tree/main/examples) for some working code examples you can run. In general, once the `VirtualEPD` object is loaded it can interact with your display using the methods described below.

### VirtualEPD Object

Objects returned by the `displayfactory` class all inherit methods from the `VirtualEPD` class. The following methods are available once the object is loaded. Be aware that not all displays may implement all methods but `display` is required.

* `width` and `height` - these are convience attributes to get the width and height of the display in your code. See the above example for their use.
* `prepare()` - does any initializing information on the display. This is waking up from sleep or doing anything else prior to a new image being drawn.
* `_display(image)` - draws an image on the display. The image must be a [Pillow Image](https://pillow.readthedocs.io/en/stable/reference/Image.html) object.
* `sleep()` - puts the display into sleep mode, if available for that device. Generally this is lower power consumption and maintains better life of the display.
* `clear()` - clears the display
* `close()` - performs any cleanup operations and closes access to the display. Use at the end of a program or when the object is no longer needed.

### Display Testing

There is a utility, `vsmp-epd-test` to verify the display. This is useful to provide users with a way their hardware is working properly. Many displays have specific library requirements that need to be installed with OS level package utilities and may throw errors until they are resolved. The test utility helps confirm all requirements are met before doing more advanced work with the display. This can be run from the command line, specifying the device from the table below.

```
# this will draw a series of rectangles
user@server:~ $ vsmp-epd-test -e vsmp_epd.mock

# this will draw the specified image
user@server:~ $ vsmp-epd-test -e vsmp_epd.mock -i /path/to/image.jpg

```

### Advanced EPD Control

There are scenarios where additional post-processing needs to be done for a particular project, or a particular display. An example of this might be to rotate the display 180 degrees to account for how the physical hardware is mounted. Another might be always adjusting the image with brightness or contrast settings. These are modifications that are specific to display requirements or user preferences and can be applied by use of a .ini file instead of having to modify code or allow for options via implementing scripts.

Two types of __ini__ files can be used in these situations. A global file, named `vsmp-epd.ini`, or a device specific file; which is the device name from the table below with a `.ini` suffix. These must exist in the root directory where the calling script is run. This is the directory given by the `os.getcwd()` method call. Valid options for this file are listed below. These will be applied on top of any processing done to the passed in image object. For example, if the implementing script is already modifying the image object to rotate 90 degrees, adding a rotate command will rotate an additional X degrees. For precedence device specific configurations trump any global configurations.

```
# file shown with default values
[EPD]
type=none  # only valid in the global configuration file, will load this display if none given to displayfactor.load_display_driver()

[Display]
rotate=0  # rotate final image written to display by X degrees [0-360]
flip_horizontal=False  # flip image horizontally
flip_vertical=False  # flip image vertically

[Image Enhancements]
color=1  # adjust the color processing, use with caution as most EPDs are black/white only. See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.convert
total_colors=2  # the total number of colors to use, only works when used with the P color mode. Useful for displays that have more than 2 colors (Inky pHhat or wHat)
contrast=1  # adjust image contrast, 1 = no adjustment
brightness=1  # adjust image brightness, 1 = no adjustment
sharpness=1  # adjust image sharpness, 1 = no adjustment
```

## Displays Implemented
Below is a list of displays currently implemented in the library. The VSMP Device Name is what you'd pass to `displaymanager.load_display_driver(deviceName)` to load the correct device driver. Generally this is the `packagename.devicename` Devices in __bold__ have been tested on actual hardware while others have been implemented but not verified. This often happens when multiple displays use the same libraries but no physical verification has happened for all models.

| Device Library | Device Name | VSMP Device Name |
|:---------------|:------------|:-----------------|
| [Inky](https://github.com/pimoroni/inky) | [Inky pHAT Red/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811) | inky.phat_red |
| | [Inky pHAT Yellow/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254905939) | inky.phat_yellow |
| | [Inky pHAT Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254938707) | inky.phat_black |
| | [Inky pHAT Red/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811) - 250x122 | inky.phat1608_red |
| | [Inky pHAT Yellow/Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254905939) - 250x122 | inky.phat1608_yellow |
| | [Inky pHAT Black/White](https://shop.pimoroni.com/products/inky-phat?variant=12549254938707) - 250x122 | inky.phat1608_black |
| | [Inky wHAT Red/Black/White](https://shop.pimoroni.com/products/inky-what?variant=13590497624147) | inky.what_red |
| | [Inky wHAT Yellow/Black/White](https://shop.pimoroni.com/products/inky-what?variant=21441988558931) | inky.what_yellow |
| | [Inky wHAT Black/White](https://shop.pimoroni.com/products/inky-what?variant=21214020436051) | inky.what_black |
| VSMP-EPD | Mock Display (emulates EPD with no hardware) | vsmp_epd.mock |
| [Waveshare](https://github.com/waveshare/e-Paper) | [1.02inch E-Ink display module](https://www.waveshare.com/1.02inch-e-Paper-Module.htm) | waveshare_epd.epdlin02 |
|  | [1.54inch E-Ink display module](https://www.waveshare.com/1.54inch-e-Paper-Module.htm) | waveshare_epd.epdlin54 <br> waveshare_epd.epdlin54_V2 |
|  | [1.54inch e-Paper Module B](https://www.waveshare.com/1.54inch-e-Paper-Module-B.htm) | waveshare_epd.epdlin54b <br> waveshare_epd.epdlin54b_V2 |
|  | [1.54inch e-Paper Module C ](https://www.waveshare.com/1.54inch-e-Paper-Module-C.htm) | waveshare_epd.epdlin54c |
|  | [2.13inch e-Paper HAT](https://www.waveshare.com/2.13inch-e-Paper-HAT.htm) | waveshare_epd. epd2in13 <br>  waveshare_epd. epd2in13_V2 |
|  | [2.13inch e-Paper HAT B](https://www.waveshare.com/2.13inch-e-Paper-HAT-B.htm) | waveshare_epd. epd2in13b_V3 |
|  | [2.13inch e-Paper HAT C ](https://www.waveshare.com/2.13inch-e-Paper-HAT-C.htm) | waveshare_epd. epd2in13bc |
|  | [2.13inch e-Paper HAT D](https://www.waveshare.com/2.13inch-e-Paper-HAT-D.htm) | waveshare_epd. epd2in13d |
|  | [2.66inch e-Paper Module](https://www.waveshare.com/2.66inch-e-Paper-Module.htm) | waveshare_epd.epd2in66 |
|  | [2.66inch e-Paper Module B](https://www.waveshare.com/2.66inch-e-Paper-Module-B.htm) | waveshare_epd.epd2in66b |
|  | [2.7inch e-Paper HAT](https://www.waveshare.com/2.7inch-e-Paper-HAT.htm) | waveshare_epd.epd2in7 |
|  | [2.7inch e-Paper HAT B](https://www.waveshare.com/2.7inch-e-Paper-HAT-B.htm) | waveshare_epd.epd2in7b <br> waveshare_epd.epd2in7b_V2 |
|  | [2.9inch e-Paper Module](https://www.waveshare.com/2.9inch-e-Paper-Module.htm) | waveshare_epd.epd2in9 <br> waveshare_epd.epd2in9_V2 <br> waveshare_epd.epd2in9b_V3 |
|  | [2.9inch e-Paper Module B](https://www.waveshare.com/2.9inch-e-Paper-Module-B.htm) | waveshare_epd.epd2in9bc |
|  | [2.9inch e-Paper Module C](https://www.waveshare.com/2.9inch-e-Paper-Module-C.htm) | waveshare_epd.epd2in9bc |
|  | [2.9inch e-Paper HAT D](https://www.waveshare.com/2.9inch-e-Paper-HAT-D.htm) | waveshare_epd.epd2in9d |
|  | [3.7inch e-Paper HAT](https://www.waveshare.com/3.7inch-e-Paper-HAT.htm) | waveshare_epd.epd3in7 |
|  | [4.2inch e-Paper Module](https://www.waveshare.com/4.2inch-e-Paper-Module.htm) |waveshare_epd.epd4in2 <br> waveshare_epd.epd4in2b_V2 |
|  | [4.2inch e-Paper Module B](https://www.waveshare.com/4.2inch-e-Paper-Module-B.htm) |waveshare_epd.epd4in2bc |
|  | [4.2inch e-Paper Module C](https://www.waveshare.com/4.2inch-e-Paper-Module-C.htm) |waveshare_epd.epd4in2bc |
|  | [5.65inch e-Paper Module F](https://www.waveshare.com/5.65inch-e-Paper-Module-F.htm) |waveshare_epd.epd5in65f |
|  | [5.83inch e-Paper HAT](https://www.waveshare.com/5.83inch-e-Paper-HAT.htm) |waveshare_epd.epd5in83 <br> waveshare_epd.epd5in83_V2 |
|  | [5.83inch e-Paper HAT B](https://www.waveshare.com/5.83inch-e-Paper-HAT-B.htm) |waveshare_epd.epd5in83b_V2 |
|  | [5.83inch e-Paper HAT C](https://www.waveshare.com/5.83inch-e-Paper-HAT-C.htm) |waveshare_epd.epd5in83bc |
|  | [7.5inch e-Paper HAT](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm) |waveshare_epd.epd7in5 <br> __waveshare_epd.epd7in5_V2__ |
|  | [7.5inch HD e-Paper HAT](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT.htm) |waveshare_epd.epd7in5_HD |
|  | [7.5inch HD e-Paper HAT B](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT-B.htm) |waveshare_epd.epd7in5b_HD |
|  | [7.5inch e-Paper HAT B](https://www.waveshare.com/7.5inch-HD-e-Paper-HAT-B.htm)| waveshare_epd.epd7in5b_V2 |
|  | [7.5inch e-Paper HAT C](https://www.waveshare.com/7.5inch-e-Paper-HAT-C.htm) | waveshare_epd.epd7in5bc |


### Display Driver Installation

Each display type has different install requirements depending on the platform.  While loading this module will install any required _Python_ libraries for supported displays; specific OS level configuration may need to be done. Basic instructions are below for each library type. Refer to instructions for your specific display to make sure you've satisfied these requirements. The `vsmp-epd-test` utility can be used to verify things are working properly.

__Inky__

Inky makes things pretty easy with a one-line installer. This makes the necessary OS level changes and pulls in the [Inky library](https://github.com/pimoroni/inky/). 

```
curl https://get.pimoroni.com/inky | bash
```

__Waveshare__

The [Waveshare device library](https://github.com/waveshare/e-Paper) requires that [SPI support](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/) be enabled on your system prior to use. The `waveshare-epd` module is automatically downloaded and installed as a dependency of this module.  

## Implementing Projects
Below is a list of known projects currently utilizing `vsmp-epd`. If you're interested in building a very small media player, check them out.

* [VSMP+](https://github.com/robweber/vsmp-plus) - My own VSMP project with a built in web server for easy administration.

## License
[GPLv3](/LICENSE)
