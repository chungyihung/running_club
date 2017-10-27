from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["os", "json", "PyQt5", "enum", "openpyxl", "sqlite3", "member", "etu", "competition" ]
excludes = ["tkinter"]

options = {
    'build_exe': {
        'packages':packages, 'excludes': excludes
    },

}

setup(
    name = "RunningClub",
    options = options,
    version = "<V1>",
    description = '<any description>',
    executables = executables
)
