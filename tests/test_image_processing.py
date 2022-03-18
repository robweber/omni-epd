import unittest
import os
import time
import glob
import pytest
from . import constants as constants
from PIL import Image, ImageChops
from shutil import copyfile
from omni_epd import displayfactory
from omni_epd.conf import CONFIG_FILE

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))

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
        self._delete_files('png')
        yield

        # clean up any files made during this test
        self._delete_files()
        self._delete_files('png')

    def setup_config(self, source_config_file_name, target_config_file_name):
        copyfile(os.path.join(TEST_PATH, 'ini', source_config_file_name), os.path.join(os.getcwd(), target_config_file_name))
        time.sleep(1)

    def open_image(self, image, w, h):
        """Open an image and resize it for EPD display"""
        result = Image.open(image)

        return result.resize((w, h))

    def compare_images(self, image_one, image_two):
        """compare if two images are equal, return true/false """
        im1 = Image.open(image_one)
        im2 = Image.open(image_two)

        diff = ImageChops.difference(im1, im2)

        if diff.getbbox() is None:
            # same
            return True
        else:
            return False

    def test_image_processing_options(self):
        """
        Test all common image processing options (rotating, contrast, etc)
        https://github.com/robweber/omni-epd#advanced-epd-control
        """

        self.setup_config(constants.ALL_IMAGE_OPTIONS, CONFIG_FILE)

        epd = displayfactory.load_display_driver(constants.GOOD_EPD_NAME)

        # write the image
        image = self.open_image(constants.GALAXY_IMAGE, epd.width, epd.height)

        epd.display(image)

    def test_basic_dither(self):
        """
        Test that a basic dither algorithm can be applied - tests that result image is different than master (non-modified) image
        Dithering will return same image if not applied or dither algorithm does not exist
        """
        self.setup_config(constants.BASIC_DITHER, CONFIG_FILE)

        epd = displayfactory.load_display_driver(constants.GOOD_EPD_NAME)

        # write the image
        image = self.open_image(constants.GALAXY_IMAGE, epd.width, epd.height)
        epd.display(image)

        # compare the two images should be different (dither applied)
        assert not self.compare_images(constants.MOCK_EPD_OUTPUT, constants.MASTER_IMAGE)
