# SlideKit - PowerPoint tools application

import os
import sys


def bundle_dir() -> str:
    """Return the app root directory, works in dev and PyInstaller-frozen modes."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
