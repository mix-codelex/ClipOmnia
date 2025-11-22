from PySide6.QtGui import QIcon
from src.utils.misc import BUTTON_ICONS
from PySide6.QtCore import Qt, QSize, Signal
from src.components.cliboard_item_struct import ClipboardItemStruct
from src.components.theme_manager import theme_manager, get_custom_item_widget_style
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton)


class NoPropagateButton(QPushButton):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        event.accept()  # stop propagation to parent widgets

class CustomItemWidget(QWidget):
    """Custom widget for QListWidgetItem with timestamp, icon, and description"""
    delete_clicked = Signal(ClipboardItemStruct)


    def __init__(self, clipboardItemStruct: ClipboardItemStruct, parent=None):
        super().__init__(parent)

        self.setObjectName("CustomItemWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.clipboardItemStruct = clipboardItemStruct
        

        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 6, 12, 6)
        main_layout.setSpacing(4)

        # Timestamp label
        self.timestamp_label = QLabel(self.clipboardItemStruct.timestamp_str)
        self.timestamp_label.setObjectName("timestampLabel")
        main_layout.addWidget(self.timestamp_label, alignment=Qt.AlignLeft)

        # Horizontal content layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)
        # content_layout.setContentsMargins(1,0,1,0)

        # Icon label
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(36, 36)
        self.icon_label.setObjectName("iconLabel")
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Set icon (image file or emoji fallback)
        if self.clipboardItemStruct.content_type == "image":
            self.icon_label.setPixmap(self.clipboardItemStruct.icon)
        else:
            self.icon_label.setText(self.clipboardItemStruct.icon)
            self.icon_label.setStyleSheet("font-size: 24px;")
            self.icon_label.setAlignment(Qt.AlignCenter)


        content_layout.addWidget(self.icon_label)

        # Description label
        self.description_label = QLabel(self.clipboardItemStruct.description)
        self.description_label.setWordWrap(True)
        self.description_label.setObjectName("descriptionLabel")
        content_layout.addWidget(self.description_label, 1)

        # Spacer + Clear button
        content_layout.addStretch()

        self.clear_button = NoPropagateButton()
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setIcon(QIcon(BUTTON_ICONS["trash"]))
        self.clear_button.setFixedSize(36, 32)
        self.clear_button.setIconSize(QSize(20, 20))
        self.clear_button.setObjectName("headerButton")
        self.clear_button.clicked.connect(self.action_button_clicked)
        content_layout.addWidget(self.clear_button)

        main_layout.addLayout(content_layout)

        self.apply_theme()
        # Listen for theme changes
        theme_manager.theme_changed.connect(self.apply_theme)


    def action_button_clicked(self):
        self.delete_clicked.emit(self.clipboardItemStruct)

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
        styles = get_custom_item_widget_style()
        self.setStyleSheet(styles)
