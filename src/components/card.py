import sys
from PySide6.QtGui import QIcon
from typing import List, Optional
from PySide6.QtCore import Qt, QSize
from src.utils.misc import BUTTON_ICONS
from src.components.theme_manager import theme_manager, get_card_style
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QMainWindow)


class Card(QWidget):
    def __init__(self, title, content_widget, tools: Optional[List[QPushButton]] = [], contentsMargins = (10, 10, 10, 10), parent=None):
        super().__init__(parent)
        self.original_parent = None
        self.original_layout = None
        self.maximize_dialog = None
        self.is_maximized = False
        self.content_widget = content_widget
        self._original_max_height = content_widget.maximumHeight()

        self.setObjectName("card")

        # ensure stylesheet background is painted
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # Outer layout with margins
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        
        # Card header
        self.card_header = QWidget()
        self.card_header.setObjectName("cardHeader")
        self.card_header.setMinimumHeight(38)
        card_header_layout = QHBoxLayout(self.card_header)
        card_header_layout.setContentsMargins(10, 0, 10, 0)

        self.card_title = QLabel(title)
        self.card_title.setObjectName("cardTitle")
        self.card_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.card_title.setFixedHeight(30)
        self.card_title.setContentsMargins(0, 0, 0, 0)

        card_header_layout.addWidget(self.card_title)
        card_header_layout.addStretch()

        for tool in tools:
            card_header_layout.addWidget(tool)


        outer_layout.addWidget(self.card_header)

        # Content area
        self.content_area = QWidget()
        self.content_area.setObjectName("Card")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(*contentsMargins)

        # Add custom content widget or create default list widget
        self.content_layout.addWidget(content_widget)

        outer_layout.addWidget(self.content_area)
        self._stored_visibility = {} 
        
        self.apply_theme()
        # 🔥 Listen for theme changes
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
        styles = get_card_style()
        self.setStyleSheet(styles)

    def toggle_maximize(self):
        if self.is_maximized:
            self._restore()
        else:
            self._maximize()

        self.is_maximized = not self.is_maximized

    def _maximize(self):
        """Show entire card in a new dialog"""
        
        if self.maximize_dialog:
            return
        
        # Remove maximum height restriction
        self.content_widget.expand_to_pixmap()
        pixmap_size = self.content_widget.get_pixmap_size()


        # Store original parent and position
        self.original_parent = self.parent()
        if self.original_parent and self.original_parent.layout():
            self.original_layout = self.original_parent.layout()
            self.original_index = self.original_layout.indexOf(self)
        
        # Create dialog
        self.maximize_dialog = QDialog(self.window())
        self.maximize_dialog.setWindowTitle(self.card_title.text())
        self.maximize_dialog.setModal(False)
        if pixmap_size:
            self.maximize_dialog.resize(pixmap_size.width(), pixmap_size.height())
            self.maximize_dialog.setFixedWidth(pixmap_size.width() + 20)
        else:
            self.maximize_dialog.resize(1000, 700)  # fallback size
        
        # Create layout for dialog
        layout = QVBoxLayout(self.maximize_dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Move entire card to dialog
        self.setParent(self.maximize_dialog)
        layout.addWidget(self)
        
        # When dialog closes, move card back
        self.maximize_dialog.finished.connect(self._restore)
        # Enable minimize + maximize + close
        self.maximize_dialog.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint |
            Qt.WindowCloseButtonHint
        )
        self.maximize_dialog.show()
    
    def _restore(self):
        """Restore card back to original parent"""
        if not self.maximize_dialog:
            return
        # Restore maximum height
        self.content_widget.restore_default_size()


        # Move card back to original parent
        if self.original_parent:
            self.setParent(self.original_parent)
            if self.original_layout:
                self.original_layout.insertWidget(self.original_index, self)
        
        # Clean up dialog
        self.maximize_dialog.deleteLater()
        self.maximize_dialog = None

    def set_title(self, title):
        """Update the card title"""
        self.card_header.setText(title)
    
    def add_widget(self, widget):
        """Add a widget to the content area"""
        self.content_layout.addWidget(widget)
    
    def clear_content(self):
        """Remove all widgets from content area"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Add search bar
        btn = QPushButton()
        btn.setIcon(QIcon(BUTTON_ICONS["camera"]))
        btn.setFixedSize(QSize(40,32))
        btn.setIconSize(QSize(24,24))
        btn.setObjectName("headerButton")

        self.clipbaord_card = Card(content_widget=btn, title="test")
        self.setCentralWidget(self.clipbaord_card)
        self.setWindowTitle("Preview")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

