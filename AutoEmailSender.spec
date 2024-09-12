# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['send_email_gui.py'],  # Replace with your main script name
    pathex=[],
    binaries=[],
    datas=[
        ('email.ico', '.'),    # Include additional files here
        ('styles.qss', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='AtuoEmailSender',   # Name of the output executable
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='email.ico'   # Specify the icon file here
          )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='AtuoEmailSender')   # Name of the final directory containing the packaged application
