# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []

for pkg in [
    'markitdown', 'markitdown.converters',
    'flask', 'werkzeug',
    'mammoth', 'puremagic', 'pdfminer', 'pptx', 'openpyxl',
    'xlrd', 'olefile', 'lxml', 'bs4', 'PIL',
    'pydub', 'speech_recognition', 'youtube_transcript_api',
    'charset_normalizer', 'certifi',
]:
    try:
        d, b, h = collect_all(pkg)
        datas         += d
        binaries      += b
        hiddenimports += h
    except Exception:
        pass  # skip packages not installed (e.g. macholib on Windows)

hiddenimports += [
    'markitdown',
    'flask',
    'werkzeug',
    'werkzeug.serving',
    'werkzeug.routing',
    'email.mime.multipart',
    'email.mime.text',
    'xml.etree.ElementTree',
    'sqlite3',
    'pydub.audio_segment',
    'speech_recognition',
    'lxml.html',
    'lxml.etree',
    'bs4',
    'PIL.Image',
    'PIL.PngImagePlugin',
    'PIL.JpegImagePlugin',
    'PIL.GifImagePlugin',
    'PIL.TiffImagePlugin',
    'PIL.BmpImagePlugin',
    'PIL.WebPImagePlugin',
    'openpyxl.cell._writer',
]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'IPython',
        'notebook',
        'pytest',
        'test',
        'unittest',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='MarkItDown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,          # UPX can corrupt .pyd extension modules on Windows
    console=False,      # No terminal window when launched from Explorer
    disable_windowed_traceback=False,
)
