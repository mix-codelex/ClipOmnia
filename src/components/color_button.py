from PySide6.QtGui import QIcon
from src.utils.misc import BUTTON_ICONS
from PySide6.QtCore import Qt, Signal, QSize
from src.components.theme_manager import theme_manager, get_menu_item_style
from PySide6.QtWidgets import (QWidget, QPushButton, QMenu, QWidgetAction, QLabel, QHBoxLayout)


class ThemeColorWidget(QWidget):
    """Custom widget showing theme name with color indicator"""
    def __init__(self, theme_name, color, parent=None):
        super().__init__(parent)
        self.theme_name = theme_name
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 2, 1, 2)
        layout.setSpacing(10)
        
        # Color indicator
        self.color_label = QLabel()
        self.color_label.setFixedSize(20, 20)
        self.color_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border: 1px solid #ccc;
                border-radius: 4px;
            }}
        """)
        
        # Theme name
        self.name_label = QLabel(theme_name)
        self.name_label.setStyleSheet("QLabel { padding: 2px; }")
        
        layout.addWidget(self.color_label)
        layout.addWidget(self.name_label)
        layout.addStretch()


class ColorDropdownButton(QPushButton):
    """Beautiful theme dropdown button with color indicators"""
    theme_changed = Signal(str)
    
    THEMES = {
        'DEFAULT': '#7a9584',
        'DARK': '#2c3e50',
        'LIGHT': '#ecf0f1',
        'OCEAN': '#1abc9c',
        'SUNSET': '#e67e22',
        'PURPLE': '#9b59b6',
        'FOREST': '#27ae60',
        'ROSE': '#e91e63',
        'MIDNIGHT': '#1a1a2e'
    }
    
    def __init__(self, btn_type="ICON", parent=None):
        super().__init__(parent)
        self.btn_type = btn_type
        self.current_theme = 'DEFAULT'
        self.menu:QMenu = QMenu(self)
        
        if self.btn_type == "ICON":
            self.setIcon(QIcon(BUTTON_ICONS["color"]))
            self.setFixedSize(QSize(40,32))
            self.setIconSize(QSize(24,24))
        else:
            self.setText(self.current_theme)
        self.setObjectName("headerButton")
        self.setCursor(Qt.PointingHandCursor)
        self._setup_menu()
        self.clicked.connect(self._show_menu)
        self.apply_theme()
        # 🔥 Listen for theme changes
        theme_manager.theme_changed.connect(self.apply_theme)

    def apply_theme(self):
        """Apply current theme to component."""
        styles = get_menu_item_style()
        self.menu.setStyleSheet(styles)

    def _setup_menu(self):
        """Create the dropdown menu with theme options"""
        # self.menu:QMenu = QMenu(self)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #e8ede9;
                border: 1px solid #2d3e34;
                border-radius: 2px;
                padding: 2px;
            }
            QMenu::separator {
                height: 1px;
                background-color: #2d3e34;
                margin: 2px 0;
            }
            QWidget:hover {
                background-color:#a8b8ad;
                border-radius: 2px;
            }
            MenuItemWidget {
                background-color: #d4ddd7;
                color: #2d3e34;
                padding: 0px;
            }
        """)
        
        # for theme_name, color in self.THEMES.items():
        for index, (theme_name, color) in enumerate(self.THEMES.items()):
            widget = ThemeColorWidget(theme_name, color)
            widget.setCursor(Qt.PointingHandCursor)
            action = QWidgetAction(self.menu)
            action.setDefaultWidget(widget)
            action.triggered.connect(lambda checked=False, t=theme_name: self._on_theme_selected(t))
            self.menu.addAction(action)
            if index < len(self.THEMES.items()) - 1:
                self.menu.addSeparator()
    
    def _show_menu(self):
        """Show the dropdown menu"""
        pos = self.mapToGlobal(self.rect().bottomLeft())
        self.menu.exec(pos)
    
    def _on_theme_selected(self, theme_name):
        """Handle theme selection"""
        if self.current_theme != theme_name:
            self.current_theme = theme_name
            self.theme_changed.emit(theme_name)
            if self.btn_type == "TEXT":
                self.setText(theme_name)
                self.current_theme = theme_name
    
    def get_current_theme(self):
        """Get the currently selected theme"""
        return self.current_theme
    
    def set_theme(self, theme_name):
        """Programmatically set the theme"""
        if theme_name in self.THEMES:
            self._on_theme_selected(theme_name)
