from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("customtkinter")

# Collect subdirectory data files
datas += collect_data_files("letterguesser.assets")
datas += collect_data_files("letterguesser.gui")
datas += collect_data_files("letterguesser.logic")
datas += collect_data_files("letterguesser.styles")

datas += [
    ("letterguesser/config.py", "letterguesser"),
    ("letterguesser/context.py", "letterguesser"),
]

a = Analysis(
    ["letterguesser/__main__.py"],
    pathex=["."],
    datas=datas,
    binaries=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="LetterGuesser",
    debug=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="dist",
)
