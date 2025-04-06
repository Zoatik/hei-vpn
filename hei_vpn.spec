# hei_vpn.spec

import os

gecko_path = os.path.join(os.getcwd(), "hei_vpn", "geckodriver")

a = Analysis(
    ['hei_vpn/main.py'],
    pathex=[],
    binaries=[(gecko_path, '.')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='hei-vpn',
    console=True,
    disable_windowed_traceback=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    icon=None,
)
