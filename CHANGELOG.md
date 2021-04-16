# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Version 0.1.3

### Added

- added `clear()` functionality to waveshare display class
- added `EPDTestUtility` class for basic display troubleshooting

### Fixed

- fixed issue when waveshare lib not installed throwing error due to import ordering

### Changed

- moved `EPDNotFoundError` class so it's easier to import

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
