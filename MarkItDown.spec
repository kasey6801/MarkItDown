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
    # markitdown 0.0.2 imports these unconditionally at module load; the
    # azure ones are namespace packages that PyInstaller's static analysis
    # regularly misses, which would crash the app before Flask starts:
    'azure.ai.documentintelligence', 'azure.identity', 'azure.core',
    'pandas', 'numpy', 'markdownify', 'requests',
]:
    try:
        d, b, h = collect_all(pkg)
        datas        += d
        binaries     += b
        hiddenimports += h
    except Exception as e:
        # Keep the build going for genuinely optional packages, but leave
        # evidence in the build log.
        print(f"WARNING: collect_all({pkg!r}) failed: {e}")

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
    [],
    exclude_binaries=True,
    name='MarkItDown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,          # UPX corrupts Python 3.14 dylibs on Apple Silicon
    console=False,      # No terminal window when launched from Finder
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='MarkItDown',
)

app = BUNDLE(
    coll,
    name='MarkItDown.app',
    icon='MarkItDown.icns',
    bundle_identifier='com.markitdown.app',
    version='0.42.1',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': True,
        'LSBackgroundOnly': False,
        'NSHumanReadableCopyright': 'MarkItDown Local — MIT License',
        'CFBundleShortVersionString': '0.42.1',
        'CFBundleVersion': '421',
        'LSMinimumSystemVersion': '12.0',
    },
)
