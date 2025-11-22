
from enum import Enum
from datetime import datetime
from PySide6.QtGui import  QPixmap
from src.components.CONTANTS import  ICON_MAP
from PySide6.QtCore import Qt, QByteArray, QBuffer

class ContentType(str, Enum):
    TEXT = "text"
    HTML = "html"
    IMAGE = "image"
    URL = "url"
    FILE = "file"
    COLOR = "color"

def is_real_html(html: str) -> bool:
    h = html.lower()

    # real document structure
    if "<html" in h or "<body" in h or "<head" in h:
        return True

    # semantic tags (not used by VS)
    semantic_tags = ("<p", "<div", "<table", "<ul", "<ol", "<li", "<br")
    if any(tag in h for tag in semantic_tags):
        return True

    # multiple block elements → definitely real HTML
    if h.count("<p") > 1 or h.count("<div") > 1:
        return True

    return False


class ClipboardItemStruct:
    """Represents one clipboard entry (text, image, url…)."""

    def __init__(self, content, content_type):
        self.content = content
        self.content_type = content_type
        self.timestamp = datetime.now()
        self.timestamp_str = self.timestamp.strftime("%H:%M:%S")

        self.icon = self._make_icon()
        self.description = self._make_description()
        self.search_text = self._make_description(make_search=True)

    def _make_icon(self):
        if self.content_type == "image":
            preview = self.content.scaled(
                32, 32,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            return QPixmap.fromImage(preview)

        return ICON_MAP.get(self.content_type, "📄")


    def _make_content_text(self):
        if self.content_type == "image":
            return f"Image ({self.content.width()}x{self.content.height()})"

        if self.content_type == "text":
            flat = self.content.replace("\n", " ")
            return flat

        if self.content_type == "url":
            return ", ".join(u.toString() for u in self.content)

        return str(self.content)
    
    def _make_description(self, make_search=False):
        if self.content_type == "image":
            return f"Image ({self.content.width()}x{self.content.height()})"

        if self.content_type == "text":
            flat = self.content.replace("\n", " ")
            if make_search:
                return flat
            else:
                return (flat[:50] + "...") if len(flat) > 50 else flat
            

        if self.content_type == "url":
            return ", ".join(u.toString() for u in self.content)

        return str(self.content)

    def digest(self):
        """Used to detect duplicates."""
        if self.content_type == "image":
            # Hash raw bytes
            ba = QByteArray()
            buffer = QBuffer(ba)
            buffer.open(QBuffer.WriteOnly)
            self.content.save(buffer, "PNG")  # deterministic
            return hash(bytes(ba))

        return hash(str(self.content))

    def __str__(self):
        return f"<ClipboardItem type={self.content_type} time={self.timestamp_str} descr={self.description}>"

    def __repr__(self):
        return f"ClipboardItem(content_type={self.content_type!r}, timestamp={self.timestamp_str!r})"
    