import os

from PyBundle import bundle_dir, resource_path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_font(font='Vera.ttf'):
    """Register fonts for report labs canvas."""
    directory = os.path.join(bundle_dir())
    ttfFile = resource_path(os.path.join(directory, font))
    if os.path.exists(ttfFile):
        pdfmetrics.registerFont(TTFont("Vera", ttfFile))
        return ttfFile
    else:
        print(ttfFile, 'can not be found')


FONT = register_font()
