# -*- mode: python ; coding: utf-8 -*-
# PyInstaller build spec for iSlide Clone
# Build: pyinstaller build.spec

import sys
from pathlib import Path

base_dir = Path('.')
resource_dir = base_dir / 'resources'

a = Analysis(
    ['main.py'],
    pathex=[str(base_dir)],
    binaries=[],
    datas=[
        ('resources/styles', 'resources/styles'),
        ('resources/config', 'resources/config'),
    ],
    hiddenimports=[
        # PyQt6
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.sip',
        # COM
        'win32com',
        'win32com.client',
        'pythoncom',
        # python-pptx
        'pptx',
        'pptx.package',
        'pptx.parts.image',
        # Image processing
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        # XML
        'lxml',
        'lxml.etree',
        # stdlib
        'xml',
        'xml.etree',
        'xml.etree.ElementTree',
        'copy',
        'io',
        'tempfile',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'IPython',
        'jupyter',
        'notebook',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SlideKit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
