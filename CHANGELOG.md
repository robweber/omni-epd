# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Version 0.1.6

### Added

- Added some notes on contributing

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
