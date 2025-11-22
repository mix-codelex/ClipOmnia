import sys
from PySide6.QtCore import QSize
from src.components.custom_item_widget import CustomItemWidget
from src.components.cliboard_item_struct import ClipboardItemStruct
from src.components.theme_manager import theme_manager, get_clipboard_list_style
from PySide6.QtWidgets import (QApplication, QMainWindow, QAbstractItemView, QListWidget, QListWidgetItem)


class ClipboardList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Customize your list
        self.setStyleSheet("background-color: white; border-radius: 5px;")
        self.setObjectName("QListWidget")
        self.setSpacing(2)
        #set visible scroball
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # Disable the default frame
        self.setFrameShape(QListWidget.NoFrame)
        
        self.apply_theme()
        # Listen for theme changes
        theme_manager.theme_changed.connect(self.apply_theme)


    # --------------------------------------------------------------
    # ADD ITEM
    # --------------------------------------------------------------
    def add_item(self, clip_item_struct: ClipboardItemStruct, index=None):
        """Add a ClipboardItemStruct to the QListWidget."""
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 65))
        widget = CustomItemWidget(clipboardItemStruct=clip_item_struct)
        
        if index:
            self.insertItem(index, item)
        else:
            self.addItem(item)
        self.setItemWidget(item, widget)
        
        return widget
    

    def remove_by_index(self, index):
        """Remove item at index."""
        if 0 <= index < self.count():
            item = self.takeItem(index)
            del item

    def clear_items(self):
        """Clear all clipboard entries."""
        self.clear()

    def get_clip_item(self, index):
        """Return the ClipboardItemStruct stored in this row."""
        if 0 <= index < self.count():
            widget = self.itemWidget(self.item(index))
            return widget.clipboardItemStruct
        return None

    def get_all_items(self):
        """Return a list of all ClipboardItemStructs."""
        items = []
        for i in range(self.count()):
            widget = self.itemWidget(self.item(i))
            items.append(widget.clipboardItemStruct)
        return items
    
    def search_item_by_text(self, search_text: str):
        """Return a list of all ClipboardItemStructs."""
        items = []
        for i in range(self.count()):
            widget: CustomItemWidget = self.itemWidget(self.item(i))
            desc_text:str = widget.clipboardItemStruct.search_text
            if search_text.lower() in desc_text.lower():
                items.append(widget.clipboardItemStruct)
        return items
    
    
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
        styles = get_clipboard_list_style()
        self.setStyleSheet(styles)


    def sizeHint(self):
        h = sum(self.sizeHintForRow(i) + self.spacing() for i in range(self.count()))
        return QSize(self.width(), h)
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.list_widget = ClipboardList()

        self.setCentralWidget(self.list_widget)
        self.setWindowTitle("Preview")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

