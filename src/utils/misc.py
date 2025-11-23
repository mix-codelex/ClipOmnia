import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller temp folder
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


BUTTON_ICONS = {
    "trash": resource_path("src/assets/icons/trash.svg"),
    "settings": resource_path("src/assets/icons/settings.svg"),
    "maximize": resource_path("src/assets/icons/maximize.svg"),
    "tool": resource_path("src/assets/icons/tool.svg"),
    "camera": resource_path("src/assets/icons/camera.svg"),
    "color": resource_path("src/assets/icons/color.svg"),
    "search": resource_path("src/assets/icons/search.svg"),
    "tray_icon": resource_path("src/assets/icon.png"),
}

