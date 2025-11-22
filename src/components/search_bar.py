import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from src.utils.misc import BUTTON_ICONS
from src.components.theme_manager import theme_manager, get_search_bar_style
from PySide6.QtWidgets import (QWidget,  QHBoxLayout, QPushButton, QLineEdit, QMainWindow, QApplication)


class SearchBar(QWidget):
    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setObjectName("search_container")
        self.TEMPLATE = None

        # ensure stylesheet background is painted
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # Outer layout with margins
        outer_layout = QHBoxLayout(self)
        outer_layout.setContentsMargins(20, 0, 20, 0)
        
        # Inner container for search components
        inner_container = QWidget()
        inner_layout = QHBoxLayout(inner_container)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)
        
        # Search icon label
        self.icon_label = QPushButton()
        self.icon_label.setIcon(QIcon(BUTTON_ICONS["search"]))
        self.icon_label.setObjectName("searchIcon")
        self.icon_label.setFixedWidth(40)
        self.icon_label.setFixedHeight(40)
        inner_layout.addWidget(self.icon_label)
        
        # Search input field
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.setFixedHeight(40)
        inner_layout.addWidget(self.search_input)
        
        outer_layout.addWidget(inner_container)

        self.apply_theme()
        # Listen for theme changes
        theme_manager.theme_changed.connect(self.apply_theme)

    def apply_override(self, **kwargs):
        """Override specific theme values."""
        base = theme_manager.get_all()
        merged = {**base, **kwargs}
        final = self.TEMPLATE.format(**merged)
        self.setStyleSheet(final)

    def set_theme(self, theme_name="DEFAULT"):
        theme_manager.set_theme(theme_name)
        self.apply_theme()

    def apply_theme(self):
        """Apply current theme to component."""
        styles = get_search_bar_style()
        self.setStyleSheet(styles)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.searchBar = SearchBar()

        self.setCentralWidget(self.searchBar)
        self.setWindowTitle("searchBar")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

