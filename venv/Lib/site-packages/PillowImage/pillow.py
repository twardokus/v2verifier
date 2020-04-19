import os
from tempfile import NamedTemporaryFile, TemporaryDirectory
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from PyBundle import bundle_dir, resource_path

from PillowImage.font import FONT
from PillowImage.utils import img_adjust


class PillowImage:
    def __init__(self, img=None, size=(792, 612), mode='RGBA', color=(255, 255, 255, 0)):
        """
        Construct an image composition using Pillow.

        :param img: Image path
        :param size: Size of new image (if img is None)
        :param mode: Mode of the new image (if img is None)
        :param color: Color of the new image (if img is None)
        """
        if img:
            # Open img and convert to RGBA color space
            self.img = Image.open(img)
            if self.img.mode != 'RGBA':
                self.img = self.img.convert('RGBA')
            else:
                self.img = self.img.copy()
        else:
            # Create a black image
            self.img = Image.new(mode, size, color=color)  # 2200, 1700 for 200 DPI
        self._tempdir = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    @property
    def tempdir(self):
        if not self._tempdir:
            self._tempdir = TemporaryDirectory(prefix='pillowimg_')
        return self._tempdir

    @property
    def size(self):
        """Return a tuple (Width, Height) with image dimensions."""
        return self.img.size

    @property
    def width(self):
        """Return the width value of the image's dimensions."""
        return self.size[0]

    @property
    def height(self):
        """Return the height value of the image's dimensions."""
        return self.size[1]

    @property
    def mode(self):
        """Return the images mode."""
        return self.img.mode

    @property
    def correct_extension(self):
        """Return the images mode."""
        return '.jpg' if self.mode != 'RGBA' else '.png'

    @property
    def longest_side(self):
        """Return the longest side value (width or height) of the image."""
        return max(self.height, self.width)

    def _text_centered_x(self, text, drawing, font_type):
        """
        Retrieve a 'x' value that centers the text in the canvas.

        :param text: String to be centered
        :param drawing: PIL.ImageDraw.Draw instance
        :param font_type: Registered font family type
        :return: X coordinate value
        """
        # ('Page Width' - 'Text Width') / 2
        return (self.width - drawing.textsize(text, font=font_type)[0]) / 2

    def _text_centered_y(self, font_size):
        """
        Retrieve a 'y' value that centers the image in the canvas.

        :param font_size: Font size
        :return: Y coordinate value
        """
        # ('Image Size' / 2) - 'Font Size'
        return (self.height / 2) - font_size

    def _img_centered_x(self, image):
        """Retrieve an 'x' value that horizontally centers the image in the canvas."""
        return int((self.width / 2) - (image.size[0] / 2))

    def _img_centered_y(self, image):
        """Retrieve an 'y' value that vertically centers the image in the canvas."""
        return int((self.height / 2) - (image.size[1] / 2))

    def image_bound(self, image, x, y):
        """
        Calculate the image bounds.

        If 'center' is found in x or y, a value that centers the image is calculated.
        If a x or y value is negative, values are calculated as that distance from the right/bottom.


        :param image: Image to-be pasted
        :param x:
        :param y:
        :return: X and Y values
        """

        def calculator(value, img_size, center_func):
            """Helper function to perform bound calculations for either x or y values."""
            # Center the image
            if 'center' in str(value).lower():
                return center_func(image)

            # Percentage value, calculate based on percentages
            elif 0 < float(value) < 1:
                return int(img_size * float(value))

            # Negative value, calculate distance from far edge (Right, Bottom
            elif int(value) < 0:
                return int(img_size - abs(value))
            else:
                return int(value)

        return (abs(calculator(x, self.width, self._img_centered_x)),
                abs(calculator(y, self.height, self._img_centered_y)))

    def scale_to_fit(self, img, func='min', scale=None, multiplier=float(1)):
        """
        Scale an image to fit the Pillow canvas.

        :param img: Image object
        :param func: Scale calculation function
        :param scale: Specific scale
        :param multiplier: Value to multiple calculated scale by
        :return:
        """
        im = img if isinstance(img, Image.Image) else Image.open(img)

        # Use either the shortest edge (min) or the longest edge (max) to determine scale factor
        if not scale:
            if func is 'min':
                scale = min(float(self.width / im.size[0]), float(self.height / im.size[1]))
            else:
                scale = max(float(self.width / im.size[0]), float(self.height / im.size[1]))
        scale = scale * multiplier

        im.thumbnail((int(im.size[0] * scale), int(im.size[1] * scale)))

        image = im if isinstance(img, Image.Image) else self.save(img=im)
        im.close()
        return image

    def resize(self, longest_side):
        """Resize by specifying the longest side length."""
        return self.resize_width(longest_side) if self.width > self.height else self.resize_height(longest_side)

    def resize_width(self, max_width):
        """Adjust an images width while proportionately scaling height."""
        width_percent = (max_width / float(self.width))
        height_size = int((float(self.height)) * float(width_percent))
        self.img = self.img.resize((max_width, height_size), Image.ANTIALIAS)
        return self.img

    def resize_height(self, max_height):
        """Adjust an images height while proportionately scaling width."""
        height_percent = (max_height / float(self.height))
        width_size = int((float(self.width) * float(height_percent)))
        self.img = self.img.resize((width_size, max_height), Image.ANTIALIAS)
        return self.img

    def draw_text(self, text, x='center', y=140, font=FONT, font_size=40, opacity=25):
        """
        Draw text onto a Pillow image canvas.

        :param text: Text string
        :param x: X coordinate value
        :param y: Y coordinate value
        :param font: Registered font family
        :param font_size: Font size
        :param opacity: Opacity of text to be drawn
        :return:
        """
        # Set drawing context
        d = ImageDraw.Draw(self.img)

        # Set a font
        fnt = ImageFont.truetype(font, int(font_size * 1.00))  # multiply size of font if needed

        # Check if x or y is set to 'center'
        x = self._text_centered_x(text, d, fnt) if 'center' in str(x).lower() else x
        y = self._text_centered_y(font_size) if 'center' in str(y).lower() else y

        # Draw text to image
        opacity = int(opacity * 100) if opacity < 1 else opacity
        d.text((x, y), text, font=fnt, fill=(0, 0, 0, opacity))

    def draw_img(self, img, x='center', y='center', opacity=1.0, rotate=0, fit=1, scale_to_fit=True,
                 scale_multiplier=float(1)):
        """
        Scale an image to fit the canvas then alpha composite paste the image.

        Optionally place the image (x, y), adjust the images opacity
        or apply a rotation.

        :param img: Path to image to paste
        :param x: X coordinates value (Left)
        :param y: Y coordinates value (Top)
        :param opacity: Opacity value
        :param rotate: Rotation degrees
        :param fit: When true, expands image canvas size to fit rotated image
        :param scale_to_fit: When true, image is scaled to fit canvas size
        :param scale_multiplier: Value to multiple calculated scale by
        :return:
        """
        img = img_adjust(img,opacity, rotate, fit, self.tempdir.name)
        with Image.open(self.scale_to_fit(img, multiplier=scale_multiplier) if scale_to_fit else img) as image:
            x, y = self.image_bound(image, x, y)
            self.img.alpha_composite(image, (x, y))

    def rotate(self, rotate):
        # Create transparent image that is the same size as self.img
        mask = Image.new('L', self.img.size, 255)

        # Rotate image and then scale image to fit self.img
        front = self.img.rotate(rotate, expand=True)

        # Rotate mask
        mask.rotate(rotate, expand=True)

        # Determine difference in size between mask and front
        y_margin = int((mask.size[1] - front.size[1]) / 3)

        # Create another new image
        rotated = Image.new('RGBA', self.img.size, color=(255, 255, 255, 0))

        # Paste front into new image and set x offset equal to half
        # the difference of front and mask size
        rotated.paste(front, (0, y_margin))
        self.img = rotated

    def save(self, img=None, destination=None, file_name='pil', ext='.png'):
        img = self.img if not img else img
        if destination:
            output = os.path.join(destination, Path(file_name).stem + ext)
        elif self.tempdir:
            tmpimg = NamedTemporaryFile(suffix='.png', dir=self.tempdir.name, delete=False)
            output = resource_path(tmpimg.name)
            tmpimg.close()
        else:
            output = os.path.join(bundle_dir(), file_name + ext)

        # Save image file
        img.save(output)
        return output

    def show(self):
        """Display a Pillow image on your operating system."""
        return self.img.show()

    def cleanup(self):
        """Implicitly delete temporary directories that have been created."""
        self.tempdir.cleanup()
