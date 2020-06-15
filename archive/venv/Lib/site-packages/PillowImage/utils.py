import os
from tempfile import NamedTemporaryFile

from PIL import Image, ImageEnhance


def img_adjust(image, opacity=1.0, rotate=None, fit=0, tempdir=None, bw=False):
    """
    Reduce the opacity of a PNG image or add rotation.

    Inspiration: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879

    :param image: PNG image file
    :param opacity: float representing opacity percentage
    :param rotate: Degrees to rotate
    :param fit: If true, expands the size of the image to fit the whole canvas
    :param tempdir: Temporary directory
    :param bw: Set image to black and white
    :return:  Path to modified PNG
    """
    # Validate parameters
    if opacity:
        try:
            assert 0 <= opacity <= 1
        except AssertionError:
            return image
    assert os.path.isfile(image), 'Image is not a file'

    # Open image in RGBA mode if not already in RGBA
    with Image.open(image) as im:
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()

        if rotate:
            # Rotate the image
            if rotate == 90:
                im = im.transpose(Image.ROTATE_90)
            elif rotate == 180:
                im = im.transpose(Image.ROTATE_180)
            elif rotate == 270:
                im = im.transpose(Image.ROTATE_270)
            else:
                im = im.rotate(rotate, expand=fit)

        # Adjust opacity
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        if bw:
            im.convert('L')

        # Save modified image file
        with NamedTemporaryFile(suffix='.png', dir=tempdir, delete=False) as dst:
            im.save(dst)
            return dst.name
