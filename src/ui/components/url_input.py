"""
URL input component for entering and testing video URLs.
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QLineEdit, 
                           QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from ...config.settings import UI_TEXTS, DEFAULT_TEST_URL, SAMPLE_VIDEO_URL


class URLInput(QWidget):
    """Widget for URL input and testing."""
    
    # Signals
    url_load_requested = pyqtSignal(str)    # Emitted when load button is clicked
    test_video_requested = pyqtSignal(str)  # Emitted when test button is clicked
    
    def __init__(self, parent=None):
        """Initialize the URL input widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the URL input UI."""
        layout = QHBoxLayout(self)
        
        # URL label
        url_label = QLabel(UI_TEXTS['url_label'])
        layout.addWidget(url_label)
        
        # URL input field
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(UI_TEXTS['url_placeholder'])
        self.url_input.setText(DEFAULT_TEST_URL)
        self.url_input.returnPressed.connect(self._on_return_pressed)
        layout.addWidget(self.url_input)
        
        # Load button
        self.load_button = QPushButton(UI_TEXTS['load_button'])
        self.load_button.clicked.connect(self._on_load_clicked)
        layout.addWidget(self.load_button)
        
        # Test video button
        self.test_button = QPushButton(UI_TEXTS['test_button'])
        self.test_button.clicked.connect(self._on_test_clicked)
        layout.addWidget(self.test_button)
        
    def _on_return_pressed(self):
        """Handle return key pressed in URL input."""
        self._on_load_clicked()
        
    def _on_load_clicked(self):
        """Handle load button click."""
        url = self.get_url()
        if url:
            self.url_load_requested.emit(url)
            
    def _on_test_clicked(self):
        """Handle test button click."""
        self.set_url(SAMPLE_VIDEO_URL)
        self.test_video_requested.emit(SAMPLE_VIDEO_URL)
        
    def get_url(self) -> str:
        """Get the current URL from the input field.
        
        Returns:
            Current URL text (stripped of whitespace)
        """
        return self.url_input.text().strip()
        
    def set_url(self, url: str):
        """Set the URL in the input field.
        
        Args:
            url: URL to set
        """
        self.url_input.setText(url)
        
    def clear_url(self):
        """Clear the URL input field."""
        self.url_input.clear()
        
    def set_placeholder_text(self, text: str):
        """Set the placeholder text for the URL input.
        
        Args:
            text: Placeholder text
        """
        self.url_input.setPlaceholderText(text)
        
    def set_load_button_enabled(self, enabled: bool):
        """Enable or disable the load button.
        
        Args:
            enabled: Whether to enable the button
        """
        self.load_button.setEnabled(enabled)
        
    def set_test_button_enabled(self, enabled: bool):
        """Enable or disable the test button.
        
        Args:
            enabled: Whether to enable the button
        """
        self.test_button.setEnabled(enabled)
        
    def set_input_enabled(self, enabled: bool):
        """Enable or disable the URL input field.
        
        Args:
            enabled: Whether to enable the input field
        """
        self.url_input.setEnabled(enabled)
        
    def focus_input(self):
        """Set focus to the URL input field."""
        self.url_input.setFocus()
        
    def select_all_text(self):
        """Select all text in the URL input field."""
        self.url_input.selectAll()
        
    def is_empty(self) -> bool:
        """Check if the URL input is empty.
        
        Returns:
            True if the input is empty, False otherwise
        """
        return not self.get_url()
        
    def set_default_url(self, url: str):
        """Set a default URL if the input is empty.
        
        Args:
            url: Default URL to set
        """
        if self.is_empty():
            self.set_url(url) 