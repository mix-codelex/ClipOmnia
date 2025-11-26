from PySide6.QtCore import QUrl, QObject, Slot, Signal, QBuffer, QByteArray, QIODevice
from PySide6.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QHttpMultiPart, QHttpPart, QNetworkReply
)
from typing import Union
import os
import json
import mimetypes

class OCRClient(QObject):
    # Signal emitted when OCR result is ready
    ocr_completed = Signal(dict)  # Emits the JSON response
    ocr_error = Signal(str)  # Emits error message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.network = QNetworkAccessManager()
        self.network.finished.connect(self.handle_reply)
        self._active_requests = {}

    def get_image_bytes(self, image_source: Union[str, bytes], filename: str = None):
        # Check if it's a file path or bytes
        if isinstance(image_source, str):
            # It's a file path
            if not filename:  # Use provided filename or derive from path
                filename = os.path.basename(image_source)
            mime, _ = mimetypes.guess_type(image_source)
            mime = mime or "image/png"
            
            with open(image_source, "rb") as f:
                file_data = f.read()
        else:
            if hasattr(image_source, "toImage"):  # QPixmap
                image_source = image_source.toImage()

            if hasattr(image_source, "save"):  # QImage
                buffer = QBuffer()
                buffer.open(QIODevice.ReadWrite)
                image_source.save(buffer, "PNG")
                file_data = buffer.data()
            else:
                # Already raw bytes / QByteArray
                file_data = QByteArray(image_source)
            
            # Use provided filename or default
            if not filename:
                filename = "image.png"
            mime = "image/png"  # Default mime type for bytes

        return file_data, filename, mime

    def send_ocr_request(self, image_source: Union[str, bytes], api_url: str = "http://localhost:8000/ocr", callback=None):
        """
        Send OCR request.
        
        Args:
            image_source: Either file path (str) or image bytes (bytes/QByteArray)
            api_url: API endpoint URL
            callback: Optional callback function(result_dict) called on success
            filename: Filename to use when sending bytes (ignored if image_source is a path)
        """
        multipart = QHttpMultiPart(QHttpMultiPart.FormDataType)
        file_data, filename, mime = self.get_image_bytes(image_source=image_source)

        # -------------------------
        # FILE PART
        # -------------------------
        file_part = QHttpPart()
        file_part.setHeader(
            QNetworkRequest.ContentDispositionHeader,
            f'form-data; name="file"; filename="{filename}"'
        )
        file_part.setHeader(
            QNetworkRequest.ContentTypeHeader,
            mime
        )
        
        file_part.setBody(file_data)
        multipart.append(file_part)

        # -------------------------
        # LANGUAGE PART
        # -------------------------
        lang_part = QHttpPart()
        lang_part.setHeader(
            QNetworkRequest.ContentDispositionHeader,
            'form-data; name="lang"'
        )
        lang_part.setBody(b"eng")
        multipart.append(lang_part)

        # -------------------------
        # POST REQUEST
        # -------------------------
        request = QNetworkRequest(QUrl(api_url))
        reply = self.network.post(request, multipart)
        
        multipart.setParent(reply)
        self._active_requests[reply] = {
            'multipart': multipart,
            'callback': callback
        }


    @Slot()
    def handle_reply(self, reply):
        request_data = self._active_requests.get(reply, {})
        callback = request_data.get('callback')
        
        # Clean up
        if reply in self._active_requests:
            del self._active_requests[reply]
        
        # Read response data
        data = reply.readAll().data()
        
        # Check for actual network errors (not NoError)
        if reply.error() != QNetworkReply.NoError:
            error_msg = f"Network Error: {reply.errorString()} (Code: {reply.error()})"
            print(error_msg)
            if data:
                print("Response body:", data.decode('utf-8', errors='replace'))
            self.ocr_error.emit(error_msg)
            reply.deleteLater()
            return

        # Parse response
        try:
            result = json.loads(data)
            # print(json.dumps(result, indent=2))
            
            # Emit signal
            self.ocr_completed.emit(result)
            
            # Call callback if provided
            if callback:
                callback(result)
                
        except Exception as e:
            error_msg = f"Invalid JSON: {e}"
            print(error_msg)
            print("Raw response:", data.decode('utf-8', errors='replace'))
            self.ocr_error.emit(error_msg)
        
        reply.deleteLater()






# Example usage:
if __name__ == "__main__":
    from functools import partial
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    # Example: Pass additional arguments to the callback
    def on_ocr_result_cb(result, image_path, some_id):
        print(f"\n=== Processing result for {image_path} (ID: {some_id}) ===")
        print(f"Text: {result.get('text')}")
        print(f"Confidence: {result.get('confidence')}")

    def on_ocr_result(result):
        print("\n=== Callback received ===")
        print(f"Text: {result.get('text')}")
        print(f"Confidence: {result.get('confidence')}")
        app.quit()
    
    def on_ocr_error(error):
        print(f"\n=== Error: {error} ===")
        app.quit()
    
    ocr = OCRClient()
    callback_with_args = partial(on_ocr_result, image_path="image.png", some_id=123)

    # Method 1
    ocr.ocr_completed.connect(on_ocr_result)
    ocr.ocr_error.connect(on_ocr_error)
    ocr.send_ocr_request("image.png")

    # Method 1. partial
    ocr.ocr_completed.connect(callback_with_args)
    ocr.ocr_error.connect(callback_with_args)
    ocr.send_ocr_request("image.png")

    # Method 2: Using callback
    ocr.send_ocr_request("image.png", callback=on_ocr_result)
    # Method 2.partial : Using callback
    ocr.send_ocr_request("image.png", callback=callback_with_args)
    
    sys.exit(app.exec())