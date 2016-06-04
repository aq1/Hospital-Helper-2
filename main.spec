# -*- mode: python -*-

block_cipher = None


a = Analysis(['app\\main.py'],
             pathex=['C:\\Users\\Jack\\Documents\\GitHub\\Hospital-Helper-2'],
             binaries=None,
             datas=[(r'C:\Users\Jack\Documents\GitHub\Hospital-Helper-2\app\gui\static\icons\*.png', r'gui\static\icons'),
             (r'C:\Users\Jack\Documents\GitHub\Hospital-Helper-2\app\gui\static\style\*.qss', r'gui\static\style'),],
             hiddenimports=[r'C:\Python34\Lib\site-packages\odf\namespaces.py'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
