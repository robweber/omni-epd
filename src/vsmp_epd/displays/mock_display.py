import logging
from .. virtualepd import VirtualEPD


# this is a reference implementation of a display extending VirtualEPD
# it does not physically write to anything but can be used as a mock testing device
class MockDisplay(VirtualEPD):
    pkg_name = 'vsmp_epd'

    def __init__(self, deviceName):
        super(MockDisplay, self).__init__(deviceName)

        # this is normally where you'd load actual device class but nothing to load here

        # set the width and height - doesn't matter since we won't write anything
        self.width = 100
        self.height = 100

    @staticmethod
    def get_supported_devices():
        # only one display supported, the test display
        return [f"{MockDisplay.pkg_name}.mock"]

    def prepare(self):
        logging.info(f"preparing {self.__str__()}")

    def display(self, image):
        logging.info(f"writing image to {self.__str__()}")

    def sleep(self):
        logging.info(f"{self.__str__()} is sleeping")

    def clear(self):
        logging.info(f"clearing {self.__str__()}")

    def close(self):
        logging.info(f"closing {self.__str__()}")
