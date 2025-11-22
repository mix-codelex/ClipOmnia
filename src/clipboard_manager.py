from typing import List, Set
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, QTimer, Signal, QMimeData
from src.components.cliboard_item_struct import ClipboardItemStruct, is_real_html


class ClipboardManager(QObject):
    updated = Signal(ClipboardItemStruct)

    def __init__(self, poll_interval=300, parent=None):
        super().__init__(parent)

        self.history: List[ClipboardItemStruct] = []
        self._ignored_digests: Set[str] = set()
        self.max_items = 30
        self._last_digest = None

        self._timer = QTimer(self)
        self._timer.setInterval(poll_interval)
        self._timer.timeout.connect(self._poll)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def _poll(self):
        cb = QApplication.clipboard()
        mime = cb.mimeData()

        item = None

        if mime.hasImage():
            item = ClipboardItemStruct(mime.imageData(), "image")

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
        self.updated.emit(item)

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
        print("IGNORE-", self._ignored_digests)
        

    def add_item_at_start(self, item: ClipboardItemStruct):
        target = item.digest()
        # Remove any existing item with the same digest
        for i, existing_item in enumerate(self.history):
            if existing_item.digest() == target:
                self.history.pop(i)
                break
        # Insert at the beginning
        self.history.insert(0, item)


    def _add_to_history(self, item: ClipboardItemStruct):
        self.history.append(item)
        if len(self.history) > self.max_items:
            self.history.pop(0)


