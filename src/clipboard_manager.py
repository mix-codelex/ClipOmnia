from typing import List, Set
from functools import partial
from src.utils.misc import str_to_bool
from PySide6.QtWidgets import QApplication
from src.settings_window import SettingsWindow
from src.utils.network_access_manager import OCRClient
from PySide6.QtCore import QObject, QTimer, Signal, QMimeData, QBuffer, QByteArray, QIODevice
from src.components.cliboard_item_struct import ClipboardItemStruct, is_real_html


class ClipboardManager(QObject):
    updated = Signal(ClipboardItemStruct)

    def __init__(self, poll_interval=300, parent=None):
        super().__init__(parent)
        self.app_settings = SettingsWindow(user_theme="DEFAULT")
        self.app_settings.setting_changed.connect(self.handle_setting_changed)
        self.ocr_client = OCRClient()
        self.current_ocr_item: ClipboardItemStruct = None

        self.history: List[ClipboardItemStruct] = []
        self._ignored_digests: Set[str] = set()
        self.max_items = 50
        self._last_digest = None

        self._timer = QTimer(self)
        self._timer.setInterval(poll_interval)
        self._timer.timeout.connect(self._poll)
        
    def handle_setting_changed(self):
        print("========== SETTINGS CHANGED ==========")
        print(self.app_settings.settings.value("ocr_mode"))
        print(self.app_settings.settings.value("user_theme"))
        print(self.app_settings.settings.value("api_url"))
        print("========== SETTINGS CHANGED ==========")

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def _poll(self):
        cb = QApplication.clipboard()
        mime = cb.mimeData()

        item = None

        if mime.hasImage():
            img_content = mime.imageData()
            item = ClipboardItemStruct(img_content, "image")

        elif mime.hasUrls():
            item = ClipboardItemStruct(mime.urls(), "url")

        elif mime.hasHtml():
            text_ = mime.text()
            if is_real_html(text_):
                item = ClipboardItemStruct(mime.html(), "html")
            else:
                item = ClipboardItemStruct(text_, "text")
            
        elif mime.hasText():
            item = ClipboardItemStruct(mime.text(), "text")

        else:
            return  # unknown type, ignore

        digest = item.digest()

        # If the clipboard content changed from the last digest
        if digest != self._last_digest:
            # Clear ignored digests for old deleted items
            self._ignored_digests.clear()

        already_exist = any(existing_item.digest() == digest for existing_item in self.history)
        if digest == self._last_digest or already_exist or digest in self._ignored_digests:
            return  # same as previous → ignore

        self._last_digest = digest

        self._add_to_history(item)
        

    def set_clipboard(self, item: ClipboardItemStruct):
        clipboard = QApplication.clipboard()
        if item.content_type == "image":
            # pixmap = QPixmap("path/to/image.png")
            clipboard.setImage(item.content) 
        elif item.content_type == "url":
            mime_data = QMimeData()
            mime_data.setUrls(item.content)
            clipboard.setMimeData(mime_data)
        else:
            clipboard.setText(item.content)


    def clear_history(self):
        self.history.clear()

    def remove_from_history(self, item: ClipboardItemStruct):
        target = item.digest()
        self.history = [x for x in self.history if x.digest() != target]
        self._ignored_digests.add(target)
        

    def add_item_at_start(self, item: ClipboardItemStruct):
        target = item.digest()
        # Remove any existing item with the same digest
        for i, existing_item in enumerate(self.history):
            if existing_item.digest() == target:
                self.history.pop(i)
                break
        # Insert at the beginning
        self.history.insert(0, item)


    def on_ocr_result(self, result, item: ClipboardItemStruct):
        # Update the item with OCR text
        updated_item = item.set_ocr_text(result.get('text'))
        
        # Insert at the beginning of history
        self.history.insert(0, updated_item)
        self.current_ocr_item = updated_item
        
        # NOW emit the updated signal with OCR text
        self.updated.emit(updated_item)
        
        # Trim history if needed
        if len(self.history) > self.max_items:
            self.history.pop(len(self.history) - 1)

    def _add_to_history(self, item: ClipboardItemStruct):
        api_url_ = self.app_settings.settings.value("api_url")
        
        if item.content_type == "image":
            if str_to_bool(self.app_settings.settings.value("ocr_mode")):
                callback_with_args = partial(self.on_ocr_result, item=item)
                self.ocr_client.send_ocr_request(item.content, api_url=api_url_, callback=callback_with_args)
            else:
                self.history.insert(0, item)
                self.updated.emit(item)
                
                if len(self.history) > self.max_items:
                    self.history.pop(len(self.history) - 1)
        else:
            self.history.insert(0, item)
            self.updated.emit(item)
            
            if len(self.history) > self.max_items:
                self.history.pop(len(self.history) - 1)

