import unittest
import os
import time
import glob
import pytest
from . import constants as constants
from PIL import Image
from shutil import copyfile
from omni_epd import displayfactory
from omni_epd.conf import CONFIG_FILE


class TestImageProcessing(unittest.TestCase):

    def _delete_files(self, file_type='ini'):
        fileList = glob.glob(os.path.join(os.getcwd(), "*." + file_type))

        for f in fileList:
            # don't bother catching errors - just let it fail out
            os.remove(f)

    @pytest.fixture(autouse=True)
    def run_before_and_after_tests(self):
        # clean up any files left over from previous tests
        self._delete_files()
        self._delete_files('.png')
        yield

        # clean up any files made during this test
        self._delete_files()
        self._delete_files('.png')

    def test_image_processing_options(self):
        """
        Test all common image processing options (rotating, contrast, etc)
        https://github.com/robweber/omni-epd#advanced-epd-control
        """

        copyfile(os.path.join(os.getcwd(), "tests", 'ini', constants.ALL_IMAGE_OPTIONS), os.path.join(os.getcwd(), CONFIG_FILE))
        time.sleep(1)

        epd = displayfactory.load_display_driver(constants.GOOD_EPD_NAME)

        # write the image
        image = Image.open(constants.GALAXY_IMAGE)

        epd.display(image)
