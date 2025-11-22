import sys
from PySide6.QtGui import QIcon
from src.components.card import Card
from src.components.CONTANTS import THEMES
from src.components.preview import Preview
from PySide6.QtCore import Qt, QSize,  QTimer
from clipboard_manager import ClipboardManager
from src.components.search_bar import SearchBar
from src.components.tool_button import ToolButton
from src.components.clipboard_list import ClipboardList
from src.components.menu_button import MenuDropdownButton
from src.components.color_button import ColorDropdownButton
from src.components.theme_manager import theme_manager, get_app_style
from src.components.cliboard_item_struct import ClipboardItemStruct
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton,
                               QListWidgetItem, QMessageBox)


class AppLayout(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard manager")
        self.setFixedSize(550, 750)   # prevent growing
        # self.setGeometry(100, 100, 900, 700)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setObjectName("centralWidget")
        main_layout.setSpacing(10)
        
        # ===== HEADER =====
        header = self.create_header()
        main_layout.addWidget(header)

        # ===== SearchBar =====
        self.search_term = ""
        self.search_bar = SearchBar("Search...")
        self.search_bar.search_input.textChanged.connect(self.handle_search_action)
        self.search_bar.search_input.returnPressed.connect(self.handle_search_action)
        # self.search_bar = self.create_search_bar()
        main_layout.addWidget(self.search_bar)

        # ===== MAIN CONTENT AREA =====
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(20, 0, 20, 0)
        
        # ===== clipbaord Card Widget =====
        self.list_widget: ClipboardList = ClipboardList()
        self.list_widget.itemClicked.connect(self.paste_item_action)
        # tools = [
        #     ToolButton(svg_file="src/assets/icons/trash.svg", callback=lambda: None),
        # ]
        self.clipbaord_card = Card( title="Clipboard", content_widget=self.list_widget, contentsMargins=(0,0,0,0))
        # Add clipbaord_card to the content_area
        content_layout.addWidget(self.clipbaord_card)
        
        # ===== Preview Card Widget =====
        self.preview = Preview()
        menu_drop_down = MenuDropdownButton(menu_items=list(self.preview.transformations.keys()), icon=QIcon("src/assets/icons/tool.svg"))
        menu_drop_down.menu_item_changed.connect(self.handle_tool_menu_item_action)
        tools = [
            menu_drop_down,
            ToolButton(svg_file="src/assets/icons/maximize.svg", callback=lambda: self.preview_card.toggle_maximize())
        ]
        self.preview_card = Card(content_widget=self.preview, title="Preview", tools=tools)
        # Add preview to the content_area
        content_layout.addWidget(self.preview_card)

        # Add contenta area to the main layout
        main_layout.addWidget(self.content_area, 1)  # stretch factor 1

        # ===== FOOTER =====
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        # Apply stylesheet
        self.apply_theme()
        # Listen for theme changes
        theme_manager.theme_changed.connect(self.apply_theme)

        # Create clipboard manager
        self.clipboard_manager = ClipboardManager()
        self.clipboard_manager.updated.connect(self.on_clipboard_update)
        self.clipboard_manager.start()

        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self._set_status_default)

    def _clear_status(self):
        self.status_label.setText("")

    def _set_status_default(self):
        self.status_label.setText(f"Monitoring clipboard... ({len(self.clipboard_manager.history)} items)")

    def handle_tool_menu_item_action(self, action: str = None):
        self.preview.apply_text_transform(action)


    def handle_search_action(self, search_text: str = None):
        if not search_text: # Handle enter & textchanged in same function
            search_text = self.search_term

        self.search_term = search_text
        self.list_widget.clear_items()
        for item in self.clipboard_manager.history:
            desc_text:str = item.search_text
            if search_text.lower() in desc_text.lower():
                widget = self.list_widget.add_item(item)
                widget.delete_clicked.connect(self.on_clipboard_item_delete)

    def on_clipboard_update(self, text):
        self.update_history_display()


    def clear_history(self):
        """Clear clipboard history"""
        reply = QMessageBox.question(self, 'Clear History', 
                                     'Are you sure you want to clear clipboard history?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.list_widget.clear_items()
            self.clipboard_manager.clear_history()
            self.preview.clear()
            self.update_status(f"Monitoring clipboard... ({len(self.clipboard_manager.history)} items)")

    def update_history_display(self):
        self.list_widget.clear_items()
        for item in self.clipboard_manager.history:
            widget = self.list_widget.add_item(item)
            widget.delete_clicked.connect(self.on_clipboard_item_delete)

        self.update_status(f"Monitoring clipboard... ({len(self.clipboard_manager.history)} items)")

    def on_clipboard_item_delete(self, item):
        self.clipboard_manager.remove_from_history(item)
        self.update_history_display()


    def paste_item_action(self, item: QListWidgetItem):
        widget = self.list_widget.itemWidget(item)
        if not widget:
            return

        item_clip: ClipboardItemStruct = widget.clipboardItemStruct
        # Only set clipboard if item still exists in history
        self.clipboard_manager.set_clipboard(item_clip)
        # Move the item in history
        self.clipboard_manager.add_item_at_start(item_clip)
        # Move the item in the QListWidget
        self.update_history_display()
        # Update selection
        self.list_widget.setCurrentItem(self.list_widget.item(0))

        if item_clip.content_type == "image":
            # Todo: make preview to see an image 
            self.preview.swap_to_image(item_clip.content) 
        elif item_clip.content_type == "url":
            # TODO: check if is a file & read file content 
            self.preview.swap_to_text(", ".join(u.toString() for u in item_clip.content)) 
        else:
            self.preview.swap_to_text(item_clip.content)

    def closeEvent(self, event):
        self.clipboard_manager.stop()
        super().closeEvent(event)

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
        styles = get_app_style()
        self.setStyleSheet(styles)

    def choose_color_theme(self, theme_name):
        self.update_status(f"Changed theme to {theme_name}...")
        theme_manager.set_theme(theme_name)

    def resizeEvent(self, event):
        new_size = event.size()  # QSize object
        print(f"Window resized to: {new_size.width()} x {new_size.height()}")
        super().resizeEvent(event)  # call the base implementation


    def create_header(self):
        """Create header widget with app name and buttons"""
        header = QWidget()
        header.setObjectName("header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # App title on the left
        app_title = QLabel("ClipOmnia")
        app_title.setObjectName("appTitle")
        header_layout.addWidget(app_title)
        
        # Spacer to push buttons to the right
        header_layout.addStretch()

        # Buttons on the right
        self.color_btn = ColorDropdownButton()
        self.color_btn.setObjectName("headerButton")
        self.color_btn.theme_changed.connect(self.choose_color_theme)
        # self.color_btn.clicked.connect(self.choose_color_theme)
        header_layout.addWidget(self.color_btn)

        clear_all_btn = QPushButton()
        clear_all_btn.setIcon(QIcon("src/assets/icons/trash.svg"))
        clear_all_btn.setFixedSize(QSize(40,32))
        clear_all_btn.setIconSize(QSize(24,24))
        clear_all_btn.setObjectName("headerButton")
        clear_all_btn.clicked.connect(self.clear_history)
        clear_all_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(clear_all_btn)
        
        return header
    
    def create_footer(self):
        """Create footer widget with status message and buttons"""
        footer = QWidget()
        footer.setObjectName("footer")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)
        
        # Status label on the left
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        footer_layout.addWidget(self.status_label)
        
        # Spacer
        footer_layout.addStretch()
        
        # Footer buttons
        settings_btn = QPushButton()
        settings_btn.setIcon(QIcon("src/assets/icons/settings.svg"))
        settings_btn.setObjectName("footerButton")
        settings_btn.setFixedSize(QSize(40,32))
        settings_btn.setIconSize(QSize(24,24))
        settings_btn.setCursor(Qt.PointingHandCursor)
        settings_btn.clicked.connect(self.open_settings)
        footer_layout.addWidget(settings_btn)
        
        return footer
    
    
    def open_settings(self):
        self.update_status("Opening settings...")
    
    
    def update_status(self, message):
        self.status_label.setText(message)

        # Restart timer every time this function is called
        self._status_timer.stop()
        self._status_timer.start(5_000)  # 5 seconds

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppLayout()
    window.show()
    sys.exit(app.exec())
