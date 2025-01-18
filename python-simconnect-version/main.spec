# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/monte/GitHub/geoshottr/images/*', 'images')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

# Define version info resource in the versioninfo block
version_info = {
    'version': '1.2',
    'product_version': '1.2',
    'file_version': '1.2.0',
    'company_name': 'GeoShottr',
    'file_description': 'GeoShottr Application',
    'product_name': 'GeoShottr',
    'internal_name': 'geoshottr',
}

# Create EXE with the version resource and desired settings
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='geoshottr',  # Set output EXE name to 'geoshottr'
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # You can set this to True if you want a console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:/Users/monte/GitHub/geoshottr/images/geoshottr.ico'],
    versioninfo=version_info,
    distpath=r'C:\Users\monte\GitHub\geoshottr\dist'
)

