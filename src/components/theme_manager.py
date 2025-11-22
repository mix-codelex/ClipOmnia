from pathlib import Path
from typing import Dict, Any
from functools import lru_cache
from src.components.CONTANTS import THEMES
from PySide6.QtCore import QObject, Signal


class ThemeManager(QObject):
    """Centralized theme management for the application."""
    theme_changed = Signal()
    
    THEMES = THEMES
    
    def __init__(self):
        super().__init__()
        self._current_theme = "DEFAULT"
        self._global_stylesheet_path = Path("styles/global.qss")
    
    @property
    def current_theme(self) -> str:
        return self._current_theme
    
    def set_theme(self, theme_name: str):

        if theme_name not in self.THEMES:
            raise ValueError(f"Theme '{theme_name}' not found")
        
        self._current_theme = theme_name

        # clear cached QSS (important!)
        get_search_bar_style.cache_clear()
        get_tool_button_style.cache_clear()
        get_preview_style.cache_clear()
        get_clipboard_list_style.cache_clear()
        get_custom_item_widget_style.cache_clear()
        get_card_style.cache_clear()
        get_app_style.cache_clear()
        get_menu_item_style.cache_clear()

        # tell everyone the theme changed
        self.theme_changed.emit()

    def get(self, key: str, default: Any = None) -> Any:
        """Get a theme value by key."""
        return self.THEMES[self._current_theme].get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all theme values for current theme."""
        return self.THEMES[self._current_theme].copy()


    def load_global_stylesheet(self) -> str:
        """Load global stylesheet if it exists."""
        if self._global_stylesheet_path.exists():
            with open(self._global_stylesheet_path, 'r') as f:
                return f.read()
        return ""
    
    def apply_theme_to_stylesheet(self, stylesheet: str) -> str:
        """Replace theme variables in a stylesheet string.
        
        Variables should be in format {variable_name}
        Example: background-color: {background};
        """
        theme = self.get_all()
        for key, value in theme.items():
            stylesheet = stylesheet.replace(f"{{{key}}}", str(value))
        return stylesheet

    def apply_theme_to_stylesheet_format(self, stylesheet: str) -> str:
        """Replace theme variables in a stylesheet string.
        
        Variables should be in format {variable_name}
        Example: background-color: {background};
        """
        theme = self.get_all()
        return stylesheet.format(**theme)

# Global theme manager instance
theme_manager = ThemeManager()


# ============= STYLE BUILDERS =============
# These functions generate component-specific styles

@lru_cache(maxsize=32)
def get_search_bar_style() -> str:
    """Generate SearchBar stylesheet."""
    return theme_manager.apply_theme_to_stylesheet("""
        #search_container {
            background-color: {background};
            border: none;
        }
        #searchIcon {
            background-color: {surface};
            color: {primary};
            font-size: 20px;
            border: 1px solid {primary};
            border-right: 1px solid {border_light};
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
        }
        #searchIcon:hover {
            background-color: {surface_hover};
        }
        #searchInput {
            background-color: {surface};
            border: 1px solid {primary};
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            padding-left: 10px;
            padding-right: 15px;
            font-size: 14px;
            color: {text};
        }
        #searchInput:focus {
            outline: none;
        }
    """)

@lru_cache(maxsize=32)
def get_tool_button_style() -> str:
    """Generate ToolButton stylesheet."""
    return theme_manager.apply_theme_to_stylesheet("""
        #headerButton {
            background-color: {surface_hover};
            border: 2px solid {surface_hover};
            border-radius: 5px;
            padding: 0px;
        }
        
        #headerButton:hover {
            background-color: {primary_light};
        }
        
        #headerButton:pressed {
            background-color: {primary_dark};
        }
    """)


@lru_cache(maxsize=32)
def get_menu_item_style() -> str:
    """Generate ToolButton stylesheet."""
    return theme_manager.apply_theme_to_stylesheet("""
        QMenu {
            background-color: {background};
            border: 1px solid {primary};
            border-radius: 2px;
            padding: 2px;
        }
        QMenu::separator {
            height: 1px;
            background-color: {primary};
            margin: 2px 0;
        }
        QWidget:hover {
            background-color: {surface_hover};
            border-radius: 2px;
        }
        MenuItemWidget {
            background-color: {border};
            color: {primary};
            padding: 0px;
        }
    """)

@lru_cache(maxsize=32)
def get_preview_style() -> str:
    """Generate ToolButton stylesheet."""
    return theme_manager.apply_theme_to_stylesheet("""
        #previewContentText {
            border: none;
            border-radius: 0px;
            background: {surface_hover};
            color: {primary};
            padding: 0px;
            margin: 0px;
            font-size: 15px;
        }
        #previewBottomText {
            background-color: {primary_light};
            color: {primary};
            font-size: 13px;
            border: none;
            border-bottom-left-radius: 5px;
            border-bottom-right-radius: 5px;
        }
    """)


@lru_cache(maxsize=32)
def get_clipboard_list_style()  -> str:
    """Generate ToolButton stylesheet."""
    return theme_manager.apply_theme_to_stylesheet("""
        QListWidget {
            background-color: transparent;
            border: none;
            outline: none;
            padding: 2px;
        }
        
        QListWidget::item {
            background-color: {background};
            border: 1px solid {primary};
            font-size: 14px;
        }
        
        QListWidget::item:hover {
            background-color: #fff;
            border-left: 4px solid {surface_hover};
        }
        
        QListWidget::item:selected {
            background-color: {surface_hover};
            border-left: 5px solid {primary};
            color: {surface_hover};
            font-weight: bold;
        }

        /* Vertical Scrollbar */
        QScrollBar:vertical {
            background: {background};
            width: 10px;
            padding: 1px;
            border-top-right-radius: 4px;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
        }
        
        QScrollBar::handle:vertical {
            background: {surface_hover};
            min-height: 30px;
            border-top-right-radius: 4px;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
        }
                            
        /* Hover */
        QScrollBar::handle:vertical:hover {
            background: {primary_light};   /* color when hovering over the handle */
        }

        /* Pressed */
        QScrollBar::handle:vertical:pressed {
            background: {primary_dark};   /* color when dragging */
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
        background: transparent;
        }
    """)


@lru_cache(maxsize=32)
def get_custom_item_widget_style()  -> str:
    """Generate ToolButton stylesheet."""
    return theme_manager.apply_theme_to_stylesheet("""
        #timestampLabel {
            color: {primary_dark};
            font-size: 10px;
        }
        #descriptionLabel {
            font-size: 12px;
            color: {primary};
        }
        #iconLabel {
            border-radius: 4px;
            border: 0.5px solid {primary_dark};
            background-color: {border};
        }
        QPushButton#headerButton {
            background-color: {border};
            border: 1px solid {primary_dark};
            border-radius: 5px;
        }
        QPushButton#headerButton:hover {
            background-color: {background};
        }
    """)


@lru_cache(maxsize=32)
def get_card_style() -> str:
    """Generate Card stylesheet."""
    return theme_manager.apply_theme_to_stylesheet("""
        #Card {
            background-color: {border};
            border: 1px solid {primary_light};
            border-bottom-left-radius: 5px;
            border-bottom-right-radius: 5px;
        }
                
        #cardTitle {
            background: transparent;
            color: {primary};
            font-size: 13px;
            border: none;
        }
        #cardHeader {
            background-color: {primary_light};
            color: {primary};
            font-size: 20px;
            border: 1px solid {primary};
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        
        #headerButton {
            background-color: {surface_hover};
            border: 2px solid {surface_hover};
            border-radius: 5px;
            padding: 0px;
        }
        
        #headerButton:hover {
            background-color: {primary_light};
        }
        
        #headerButton:pressed {
            background-color: {primary_dark};
        }
    """)

@lru_cache(maxsize=32)
def get_app_style() -> str:
    """Generate main application stylesheet."""
    return theme_manager.apply_theme_to_stylesheet("""
        #centralWidget {
            background-color: {background};
        }
        #contentArea {
            background-color: {background};
        }
        

        #header {
            background-color: {primary_light};
            min-height: 60px;
            max-height: 60px;
        }
        
        #appTitle {
            color: {primary};
            font-size: 20px;
            font-weight: bold;
        }
        
        #headerButton {
            background-color: {surface_hover};
            border: 2px solid {surface_hover};
            border-radius: 5px;
            padding: 0px;
        }
        
        #headerButton:hover {
            background-color: {primary_light};
        }
        
        #headerButton:pressed {
            background-color: {primary_dark};
        }
        
        #footer {
            background-color: {primary_light};
            min-height: 50px;
            max-height: 50px;
        }
        
        #statusLabel {
            color: {primary};
            font-size: 13px;
        }
        
        #footerButton {
            background-color: {surface_hover};
            border: 2px solid {surface_hover};
            border-radius: 5px;
        }
        
        #footerButton:hover {
            background-color: {primary_light};
        }

        #footerButton:pressed {
            background-color: {primary_dark};
        }
        
        QListWidget {
            border: 1px solid #ddd;
            border-radius: 5px;
        }
    """)

