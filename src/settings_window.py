from PySide6.QtCore import QSettings, Signal
from src.components.theme_manager import theme_manager
from src.components.color_button import ColorDropdownButton
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox,
    QRadioButton, QButtonGroup
)


class SettingsWindow(QDialog):
    setting_changed = Signal()

    def __init__(self, user_theme, api_url: str = "http://localhost:8000/ocr"):
        super().__init__()

        self.setWindowTitle("Settings")
        self.settings = QSettings("MyCompany", "MyApp")
        self.settings.setValue("user_theme", user_theme)
        self.settings.setValue("api_url", api_url)
        self.settings.setValue("ocr_mode", True)

        # Widgets
        self.current_theme = user_theme
        self.user_theme = ColorDropdownButton(btn_type="TEXT")
        self.user_theme.setObjectName("headerButton")
        self.user_theme.theme_changed.connect(self.choose_color_theme)

        self.api_url = QLineEdit()
        self.api_url.setText(self.settings.value("api_url", ""))


        # --- Radio buttons for OCR mode ---
        self.ocr_text_radio = QRadioButton("OCR")
        self.image_radio = QRadioButton("Image")
        
        # Load previous setting if exists
        saved_mode = self.settings.value("ocr_mode", True)
        if saved_mode:
            self.ocr_text_radio.setChecked(True)
        else:
            self.image_radio.setChecked(True)

        self.ocr_group = QButtonGroup()
        self.ocr_group.addButton(self.ocr_text_radio)
        self.ocr_group.addButton(self.image_radio)

        # OK / Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Theme:"))
        layout.addWidget(self.user_theme)

        layout.addWidget(QLabel("Api url:"))
        layout.addWidget(self.api_url)

        layout.addWidget(QLabel("OCR Mode:"))
        layout.addWidget(self.ocr_text_radio)
        layout.addWidget(self.image_radio)

        layout.addWidget(buttons)

        self.setLayout(layout)


    def choose_color_theme(self, theme_name):
        theme_manager.set_theme(theme_name)
        self.current_theme = theme_name
        

    def accept(self):
        self.settings.setValue("user_theme", self.current_theme)
        self.settings.setValue("api_url", self.api_url.text())
        mode = True if self.ocr_text_radio.isChecked() else False
        self.settings.setValue("ocr_mode", mode)
        self.setting_changed.emit()
        return super().accept()
