import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from src.utils.text_transformation import to_lower, to_upper, to_capitalize
from src.components.theme_manager import theme_manager, get_preview_style
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow, QVBoxLayout, QTextEdit, QSizePolicy)


class Preview(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.setObjectName("preview_container")
        self.setFixedHeight(250)
        self.pixmap = None
        self.transformations = {
            "Lowercase": to_lower,
            "Uppercase": to_upper,
            "Capitalize": to_capitalize
        }

        # Outer layout with margins
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        

        # Content area
        self.content_area = QWidget()
        self.content_area.setObjectName("previewContent")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Add content widget
        self.text_edit_area = QTextEdit()
        self.text_edit_area.setObjectName("previewContentText")
        self.content_layout.addWidget(self.text_edit_area)
        outer_layout.addWidget(self.content_area)

        # Preview Bottom text
        # self.preview_bottom_text = QLabel("News article text/nature image")
        # self.preview_bottom_text.setObjectName("previewBottomText")
        # self.preview_bottom_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # self.preview_bottom_text.setMinimumHeight(25)
        # self.preview_bottom_text.setContentsMargins(5, 0, 0, 0)
        # # self.set_text("Preview content...")
        # outer_layout.addWidget(self.preview_bottom_text)

        self.apply_theme()
        # Listen for theme changes
        theme_manager.theme_changed.connect(self.apply_theme)
    

    def apply_text_transform(self, action: str):
        if not isinstance(self.text_edit_area, QTextEdit):
            return
        
        transform_fn = self.transformations[action]
        cursor = self.text_edit_area.textCursor()
        selected = cursor.selectedText()

        if selected:
            transformed = transform_fn(selected)
            cursor.insertText(transformed)
        else:
            # No selection → transform full text
            full = self.text_edit_area.toPlainText()
            transformed = transform_fn(full)
            self.text_edit_area.setPlainText(transformed)

    # ------------------------------
    # Swap to image
    # ------------------------------
    def swap_to_image(self, image: QImage):
        # Remove old widget
        self.content_layout.removeWidget(self.text_edit_area)
        self.text_edit_area.setParent(None)

        # Create QLabel to show the image
        self.text_edit_area = QLabel()
        self.text_edit_area.setObjectName("previewContentText")
        self.text_edit_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set image
        self.pixmap = QPixmap.fromImage(image)
        self.text_edit_area.setPixmap(self.pixmap)
        self.text_edit_area.setScaledContents(True)
    

        # Add QLabel to layout
        self.content_layout.addWidget(self.text_edit_area)



    # ------------------------------
    # Swap back to text
    # ------------------------------
    def swap_to_text(self, text: str = ""):
        # Remove old widget
        self.pixmap = None
        self.content_layout.removeWidget(self.text_edit_area)
        self.text_edit_area.setParent(None)

        # Create QTextEdit
        self.text_edit_area = QTextEdit()
        self.text_edit_area.setObjectName("previewContentText")
        self.text_edit_area.setText(text)

        # Add QTextEdit to layout
        self.content_layout.addWidget(self.text_edit_area)

    def clear(self):
        if isinstance(self.text_edit_area, QTextEdit):
            self.text_edit_area.clear()       # clear text content
        elif isinstance(self.text_edit_area, QLabel):
            self.text_edit_area.setPixmap(QPixmap())  # clear image
            self.text_edit_area.setText("")           # clear text if any


    def expand_to_pixmap(self):
        """Set widget to freely expand to the pixmap's size."""
        if isinstance(self.text_edit_area, QLabel) and self.pixmap:
            size = self.pixmap.size()
            # Set maximum size to match pixmap
            self.setMaximumSize(size)
            # Let it expand inside layout
            self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        elif isinstance(self.text_edit_area, QTextEdit):
            # Remove maximum height restriction
            self.setMaximumHeight(16777215)  # effectively no limit
            self.setMaximumWidth(16777215)
            # Allow QTextEdit to expand in layout
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            
    def get_pixmap_size(self):
        if self.pixmap:
            return self.pixmap.size()  # returns QSize
        return None

    def restore_default_size(self):
        self.setMaximumHeight(250)  # original fixed height
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def clear_(self):
        self.text_edit_area.clear()

    def set_text(self, text):
        """Update the card title"""
        self.text_edit_area.setText(text)
        
    def set_text_plain(self, text):
        """Update the card title"""
        self.text_edit_area.setPlainText(text)

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
        styles = get_preview_style()
        self.setStyleSheet(styles)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.preview = Preview()

        self.setCentralWidget(self.preview)
        self.setWindowTitle("Preview")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

