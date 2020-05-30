import os
import unittest

from looptools import Timer

from PillowImage import PillowImage
from tests import *


class TestPillowImagePNG(unittest.TestCase):
    result_dir = init_result_dir('png')
    
    @classmethod
    def setUpClass(cls):
        cls.img_path = IMG_PATH
        cls.wtrmrk_path = WTR_PATH
        cls.pdf = None

    @Timer.decorator
    def test_draw_text(self):
        """Draw text onto an image."""
        with PillowImage() as draw:
            draw.draw_text('Here is the first text', y=10, opacity=50)
            draw.draw_text('Here is the second text', y=50, opacity=50)
            d = draw.save(destination=self.result_dir, file_name='draw_text')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_draw_img(self):
        """Draw text onto an image."""
        with PillowImage() as draw:
            draw.draw_img(self.img_path)
            draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30)
            d = draw.save(destination=self.result_dir, file_name='draw_img')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_draw_img_overlay(self):
        """Draw text onto an image."""
        with PillowImage(img=self.img_path) as draw:
            draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30)
            d = draw.save(destination=self.result_dir, file_name='draw_img_overlay')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_draw_img_centered(self):
        """Draw text onto an image."""
        with PillowImage(img=self.img_path) as draw:
            draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30, x='center', y='center')
            d = draw.save(destination=self.result_dir, file_name='draw_img_centered')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_draw_img_negbound(self):
        """Draw text onto an image."""
        with PillowImage(img=self.img_path) as draw:
            draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30, x=-2000, y=-2000)
            d = draw.save(destination=self.result_dir, file_name='draw_img_negbound')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_draw_img_percentage(self):
        """Draw text onto an image."""
        with PillowImage(img=self.img_path) as draw:
            draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30, x=.5, y=.1)
            d = draw.save(destination=self.result_dir, file_name='draw_img_percentage')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_draw_img_resized(self):
        """Draw text onto an image."""
        longest_side = 500
        with PillowImage(img=self.img_path) as draw:
            draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30)
            draw.resize(longest_side)
            d = draw.save(destination=self.result_dir, file_name='draw_img_resized')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert actual longest edge is equal to target longest edge
        self.assertEqual(longest_side, draw.longest_side)
        return d

    @Timer.decorator
    def test_draw_img_resize_width(self):
        """Draw text onto an image."""
        width = 300
        with PillowImage(img=self.img_path) as draw:
            draw.resize_width(width)
            d = draw.save(destination=self.result_dir, file_name='draw_img_resized_width')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert actual longest edge is equal to target longest edge
        self.assertEqual(width, draw.width)
        return d

    @Timer.decorator
    def test_draw_img_resize_height(self):
        """Draw text onto an image."""
        height = 300
        with PillowImage(img=self.img_path) as draw:
            draw.resize_height(height)
            d = draw.save(destination=self.result_dir, file_name='draw_img_resized_height')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert actual longest edge is equal to target longest edge
        self.assertEqual(height, draw.height)
        return d

    @Timer.decorator
    def test_rotate(self):
        """Draw text onto an image."""
        with PillowImage() as draw:
            draw.draw_img(self.img_path)
            draw.rotate(30)
            d = draw.save(destination=self.result_dir, file_name='rotate')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_size(self):
        """Draw text onto an image."""
        with PillowImage(img=self.img_path) as draw:
            size = draw.size
            d = draw.save(destination=self.result_dir, file_name='size')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert image size is correct
        self.assertIsInstance(size, tuple)
        self.assertTrue(size == (2706, 2226))
        return d

    @Timer.decorator
    def test_width(self):
        """Draw text onto an image."""
        with PillowImage(img=self.img_path) as draw:
            width = draw.width
            d = draw.save(destination=self.result_dir, file_name='width')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert image size is correct
        self.assertTrue(width == 2706)
        return d

    @Timer.decorator
    def test_height(self):
        """Draw text onto an image."""
        with PillowImage(img=self.img_path) as draw:
            height = draw.height
            d = draw.save(destination=self.result_dir, file_name='height')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert image size is correct
        self.assertTrue(height == 2226)
        return d


if __name__ == '__main__':
    unittest.main()
