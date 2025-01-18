main
# This file is the configuration file for PyInstaller.
# FILE: /python-automation-project/python-automation-project/pyinstaller.spec
version-2.1
block_cipher = None

a = Analysis(['src/app.py'],
             pathex=['.'],
             binaries=[],
             datas=[('src/templates/index.html', 'templates')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
           cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='python_automation_project',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='python_automation_project')