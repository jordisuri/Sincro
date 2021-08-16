# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['est├á', 'en', 'el', 'D:\\Prog\\Python\\Scripts\\;D:\\Prog\\Python\\;C:\\Program', 'Files', '(x86)\\Common', 'Files\\Oracle\\Java\\javapath;C:\\ProgramData\\Oracle\\Java\\javapath;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\Program', 'Files', '(x86)\\Intel\\OpenCL', 'SDK\\2.0\\bin\\x86;C:\\Program', 'Files', '(x86)\\Intel\\OpenCL', 'SDK\\2.0\\bin\\x64;D:\\Aplics\\Prog\\Llenguatges\\Scripts\\;D:\\Aplics\\Prog\\Llenguatges\\Python3;C:\\adb;C:\\Program', 'Files\\Intel\\WiFi\\bin\\;C:\\Program', 'Files\\Common', 'Files\\Intel\\WirelessCommon\\;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\WINDOWS\\System32\\OpenSSH\\;C:\\Program', 'Files\\dotnet\\;D:\\Aplics\\Video\\QuickTime', 'Alternative\\QTSystem;C:\\Program', 'Files', '(x86)\\Windows', 'Live\\Shared;C:\\Program', 'Files', '(x86)\\Windows', 'Kits\\10\\Windows', 'Performance', 'Toolkit\\;D:\\Aplics\\Utilitats\\Git\\cmd;D:\\Aplics\\Prog\\Llenguatges\\;C:\\Users\\Jordi\\AppData\\Local\\Microsoft\\WindowsApps'],
             pathex=['C:\\Users\\Jordi\\Desktop\\Sincro'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          name='est├á',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='est├á')
