import os
import unittest

from looptools import Timer

from PillowImage import img_adjust
from tests import *


class TestPillowImageUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = IMG_PATH
        cls.wtrmrk_path = WTR_PATH
        cls.pdf = None

    def setUp(self):
        self.image = None

    def tearDown(self):
        os.remove(self.image)

    @Timer.decorator
    def test_img_adjust_rotate(self):
        """Test the function 'img_rotate.'"""
        self.image = img_adjust(self.wtrmrk_path, rotate=30, fit=1)

        # Assert file exists
        self.assertTrue(os.path.exists(self.image))
        return self.image


if __name__ == '__main__':
    unittest.main()
