# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

block_cipher = None

project_root = Path.cwd()


def add_data_if_present(src, dest):
    source_path = project_root / src
    if not source_path.exists():
        return None
    if source_path.is_dir() and not any(source_path.iterdir()):
        return None
    return (src, dest)


added_files = [
    item for item in [
        add_data_if_present('courses', 'courses'),
        add_data_if_present('saves', 'saves'),
        add_data_if_present('README.md', '.'),
        add_data_if_present('practice_exam_template.json', '.'),
    ] if item is not None
]

a = Analysis(
    ['exam_gui.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PracticeExamGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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
    upx=True,
    upx_exclude=[],
    name='PracticeExamGenerator',
)
