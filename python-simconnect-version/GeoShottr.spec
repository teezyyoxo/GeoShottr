# -*- mode: python ; coding: utf-8 -*-
# Read version from version.py without importing
import re
with open('version.py', 'r') as f:
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', f.read())
    __version__ = version_match.group(1) if version_match else "1.8.0"


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('../images', 'images'), ('version.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=f'GeoShottr{__version__}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['../images/geoshottr.ico'],
)
