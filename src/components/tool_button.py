from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import ( QPushButton )
from src.components.theme_manager import theme_manager, get_tool_button_style

class ToolButton(QPushButton):
    def __init__(self, svg_file, callback=None, parent=None):
        super().__init__(parent)

        self.callback = callback   # store the function so parent can access it
        self.setObjectName("headerButton")

        self.setIcon(QIcon(svg_file))
        self.setFixedSize(QSize(36, 28))
        self.setIconSize(QSize(20, 20))
        self.setCursor(Qt.PointingHandCursor)

        # connect the click event to an internal handler
        self.clicked.connect(self._on_clicked)

        self.apply_theme()
        # 🔥 Listen for theme changes
        theme_manager.theme_changed.connect(self.apply_theme)

    def _on_clicked(self):
        """Wrapper so we can control the call signature."""
        if callable(self.callback):
            self.callback()

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
        styles = get_tool_button_style()
        self.setStyleSheet(styles)
