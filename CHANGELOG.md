# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Version 0.3.4

### Added

- `palette_filter` advanced option now supports [color names](https://github.com/python-pillow/Pillow/blob/e3cb4bb8e00fcaf4c3e0783f7c02e51372595659/src/PIL/ImageColor.py#L153-L305) or hex values in addition to RGB colors. Thanks @missionfloyd

## Version 0.3.3

### Added

- added link to [pycasso](https://github.com/jezs00/pycasso) in the README. Thanks @jezs00
- new displays, [Waveshare 7.3in 7 Color](https://www.waveshare.com/7.3inch-e-paper-hat-f.htm) - thanks @evelyndooley, [Waveshare 2.13in V3](https://www.waveshare.com/2.13inch-e-paper-hat.htm)

## Version 0.3.2

### Changed

- updated Pillow min version to 9.1+
- code cleanup for proper style standards - thanks @missionfloyd

### Added

- added new 4 color waveshare displays (epd1in64g, epd2in36g, epd3in0g, epd4in37g, epd7in3g). Thanks @missionfloyd

## Version 0.3.1

### Added

- `omni_epd.mock` can now set both the width and height values within the `.ini` file. Thanks @missionfloyd

### Fixed

- `omni_epd.mock` device now returns a palette filter when using the color mode. Previously this returned only b/w and resulted in image processing enhancements resulting in a black and white only image, even when color was selected. Hardcoded palette based on web safe colors.

- Waveshare device `epd2in13_V2` should use the alternate clear method which requires a color parameter. Thanks @ThatIsAPseudo for pointing this out

### Changed

- dithering is now done with [didder](https://github.com/makeworld-the-better-one/didder) - this is a massive improvement both in scope and speed to hitherdither. Thanks @missionfloyd

### Removed

- removed `hitherdither` as a dependency

## 0.3.0

### Added

- added `force_palette` argument to the `virtualepd._filter()` function. Will force palette based conversion if wanted, default is False
- added additional tested displays per #63 comments
- new unit tests to make sure image processing components run without error
- support for `inky.auto` as a valid EPD device. This will auto detect Inky devices and load the correct driver. Thanks @donbing
- support for IT8951 devices, such as the WaveShare 6in display

### Fixed

- calls to `Image.quantize` require an RGB or L mode Image object, convert any loaded image before applying new palettes
- when filling palette too many colors were being set (< 256), wrong length variable was being used
- fixed regression where Inky `bw` mode was causing colors to be inverted
- universal fix for Waveshare Tri-color displays as original fixes broke some displays - thanks @aaron8684

### Changed

- make sure Pillow and Inky packages are known working versions or above - thanks @donbing
- `bw` standardized as the consistent naming for the default black/white device mode. `black` will throw a warning, affects Inky devices - thanks @missionfloyd

## 0.2.6

### Added

- added `version` identifier for Waveshare devices so that V2 and V3 boards can be identified from the others

### Fixed

- fixed typos in 5.65in Waveshare implementation - thanks @aaronr8684
- fixed issues with BW display on 7.5 tri-color screens - thanks @aaronr8684

### Removed

- removed dependency inky[fonts], this is not needed. Thanks @missionfloyd

## Version 0.2.5

### Fixed

- fixed overlay colors in epd5in83c tri-color display (thanks @dr-boehmerie)

### Added

- `waveshare_epd.epd2in9` and `waveshare_epd.epd5in83c` are now tested (thanks @dr-boehmerie)

## Version 0.2.4

### Fixed

- fixed issues with Waveshare 3.7in devices not working properly.

## Version 0.2.3

### Added

- dithering options in `ini` file added using the [hitherdither](https://github.com/hbldh/hitherdither) library, thanks @missionfloyd

## Version 0.2.2

### Added

- added [SlowMovie](https://github.com/TomWhitwell/SlowMovie) to list of implementing projects

### Changed

- modified several of the Waveshare devices to make sure `init()`, `display()`, and `clear()` methods are all being called correctly based on device specifics

## Version 0.2.1

### Changed

- restructured object inheritance to reduce duplicate code, this is especially true for waveshare devices

### Fixed

- fixed issue where test utility would fail on inky displays. made the `draw()` function more universal between devices

## Version 0.2.0

### Added

- added device specific modes to INI file
- updated device types to use multiple color modes when available
- added many device specific options, loaded within INI files. [Documented on wiki](https://github.com/robweber/omni-epd/wiki/Device-Specific-Options)
- Inky Impression is tested - thanks @missionfloyd

### Changed

- updated device table to show available device modes for each supported type
- dynamically load class files instead of using import where possible
- changed example image to use one from NASA with more colors for better color display test
- updated tests to better handle INI file cleanup

### Removed

- removed Image Enhancements from INI having to do with colors, moved to device specific configurations

## Version 0.1.7

### Added

- The mock display driver, `omni_epd.mock`, now writes the image file to a jpg in the local directory for better testing

### Fixed

- EPD config section didn't have corresponding var in `conf.py`
- fixed issues with some Waveshare displays not working due to differences in individual drivers #8 for more details

## Version 0.1.6

### Added

- Added some notes on contributing
- unit test build badge to README

### Changed

- Rebrand! `vsmp-epd` renamed to `omni-epd`, subsequent commands and documentation also updated

## Version 0.1.5

### Added

- support for Inky type displays (pHAT, wHAT, and Impression)
- added instructions for installing direct from repo

### Removed

- removed PyPi setup instructions, more important to allow installing of waveshare libs

## Version 0.1.4

### Added

- added ability to create `vsmp-epd.ini` file to manually set display options for epd that always get applied
- added device level ini file using `devicename.ini` for syntax
- automatic pytest checks for PRs on Github Actions
- added working code examples
- `vsmp-epd-test` now accepts the `-i` flag to load an image in addition to the default display pattern

### Changed

- don't use the root logger
- added additional VirtualEPD class logging
- modified `setup.cfg` to add additional [Classifiers](https://pypi.org/classifiers/) and correct dependencies (waveshare from git)

## Version 0.1.3

### Added

- added `clear()` functionality to waveshare display class
- added `EPDTestUtility` class for basic display troubleshooting
- added `vsmp-epd-test` console script for quick user testing

### Fixed

- fixed issue when waveshare lib not installed throwing error due to import ordering

### Changed

- moved `EPDNotFoundError` class so it's easier to import
- updated README with better individual display and testing instructions

## Version 0.1.2

### Fixed

- missed some debug messages and syntax errors

## Version 0.1.1

### Added

- added some license notices per gnu.org
- added some unit tests

### Changed

- invalid device now throws `EPDNotFoundError` instead of calling exit - let the user deal with it

## Version 0.1.0 - 2021-04-15

### Added

- Pypi badge with most current version

### Changed

- small tweaks to create a decent release version for PyPi

## Version 0.0.3 - 2021-04-15

### Changed

- Added information on supported displays and usage information to README

### Fixed

- fixed waveshare `close()` behavior

## Version 0.0.2 - 2021-04-14

### Added

- added project config files like .gitignore, README, License, etc
- added python project build files (setup.py, setup.cfg, etc)

### Changed

- updated legacy class files for better package management
