from typing import List
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal, QSize
from src.components.theme_manager import theme_manager, get_menu_item_style
from PySide6.QtWidgets import (QWidget, QPushButton, QMenu, QWidgetAction, QLabel, QHBoxLayout)


class MenuItemWidget(QWidget):
    """Custom widget showing theme name with color indicator"""
    def __init__(self, menu_item_name, parent=None):
        super().__init__(parent)
        self.menu_item_name = menu_item_name
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)
        
        # Theme name
        self.name_label = QLabel(menu_item_name)
        self.name_label.setStyleSheet("QLabel { padding: 2px; }")
        
        layout.addWidget(self.name_label)
        layout.addStretch()


class MenuDropdownButton(QPushButton):
    """Beautiful theme dropdown button with color indicators"""
    menu_item_changed = Signal(str)
    def __init__(self, menu_items: List[str], icon: QIcon, parent=None):
        super().__init__(parent)
        self.menu_items = menu_items
        self.current_menu_item = None
        self.menu: QMenu = QMenu(self)
        
        self.setIcon(icon)
        self.setFixedSize(QSize(36, 28))
        self.setIconSize(QSize(20, 20))
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
        for index, menu_item_name in enumerate(self.menu_items):
            widget = MenuItemWidget(menu_item_name)
            # Set cursor to pointer on hover
            widget.setCursor(Qt.PointingHandCursor)

            # 🔥 wrapper that centers the widget horizontally
            container = QWidget()
            hbox = QHBoxLayout(container)
            hbox.setContentsMargins(0, 0, 0, 0)   # slight padding for beauty
            hbox.addStretch()
            hbox.addWidget(widget)
            hbox.addStretch()

            action = QWidgetAction(self.menu)
            action.setDefaultWidget(container)
            action.triggered.connect(lambda checked=False, t=menu_item_name: self._on_theme_selected(t))
            self.menu.addAction(action)
            # Add separator after specific position (adjust index as needed)
            # Example: Add divider after 3rd item (index 2)
            if index < len(self.menu_items) - 1:
                self.menu.addSeparator()

    def _show_menu(self):
        """Show the dropdown menu"""
        pos = self.mapToGlobal(self.rect().bottomLeft())
        self.menu.exec(pos)
    
    def _on_theme_selected(self, menu_item_name):
        """Handle theme selection"""
        self.current_menu_item = menu_item_name
        self.menu_item_changed.emit(menu_item_name)
    
    def get_current_menu_item(self):
        """Get the currently selected theme"""
        return self.current_menu_item
    