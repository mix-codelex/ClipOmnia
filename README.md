# ClipOmina


# Dependencies 

poetry add PySide6==6.10.1 PySide6-Addons==6.10.1 PySide6-Essentials==6.10.1
pipenv install PySide6==6.10.1 PySide6-Addons==6.10.1 PySide6-Essentials==6.10.1 pyinstaller==6.16.0


pipenv install pyinstaller==6.16.0
pyinstaller --onefile --windowed main.py
pyinstaller --onefile --windowed --icon=src/icon.ico main.py
pyinstaller --onefile --windowed --icon=resources/icon.ico --add-data "src/assets;src/assets" main.py


icon=QIcon("src/assets/icons/tool.svg")
