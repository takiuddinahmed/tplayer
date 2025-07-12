"""
Debug console component for displaying debug messages.
"""

from PyQt5.QtWidgets import QTextEdit, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from ...config.settings import DEBUG_CONSOLE_HEIGHT, UI_TEXTS


class DebugConsole(QTextEdit):
    """Debug console widget for displaying log messages."""
    
    def __init__(self, parent=None):
        """Initialize the debug console.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the debug console UI."""
        self.setMaximumHeight(DEBUG_CONSOLE_HEIGHT)
        self.setReadOnly(True)
        
        # Set initial text
        self.setPlainText(f"{UI_TEXTS['debug_console_title']}\n")
        
        # Style the console
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Courier New', monospace;
                font-size: 10px;
                border: 1px solid #555555;
            }
        """)
        
    def append_message(self, message: str):
        """Append a message to the debug console.
        
        Args:
            message: Message to append
        """
        self.append(message)
        
        # Auto-scroll to bottom
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        
    def clear_console(self):
        """Clear all messages from the console."""
        self.clear()
        self.setPlainText(f"{UI_TEXTS['debug_console_title']}\n")
        
    def append_error(self, message: str):
        """Append an error message with special formatting.
        
        Args:
            message: Error message to append
        """
        self.append(f"[ERROR] {message}")
        
    def append_warning(self, message: str):
        """Append a warning message with special formatting.
        
        Args:
            message: Warning message to append
        """
        self.append(f"[WARNING] {message}")
        
    def append_info(self, message: str):
        """Append an info message with special formatting.
        
        Args:
            message: Info message to append
        """
        self.append(f"[INFO] {message}")
        
    def append_debug(self, message: str):
        """Append a debug message with special formatting.
        
        Args:
            message: Debug message to append
        """
        self.append(f"[DEBUG] {message}")
        
    def set_max_lines(self, max_lines: int):
        """Set maximum number of lines to keep in the console.
        
        Args:
            max_lines: Maximum number of lines
        """
        # Get current text
        text = self.toPlainText()
        lines = text.split('\n')
        
        # Keep only the last max_lines
        if len(lines) > max_lines:
            lines = lines[-max_lines:]
            self.setPlainText('\n'.join(lines))
            
        # Auto-scroll to bottom
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        
    def save_to_file(self, filename: str):
        """Save console content to a file.
        
        Args:
            filename: File path to save to
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.toPlainText())
            self.append_info(f"Console saved to {filename}")
        except Exception as e:
            self.append_error(f"Failed to save console: {str(e)}")
            
    def get_content(self) -> str:
        """Get the current console content.
        
        Returns:
            Console content as string
        """
        return self.toPlainText()
        
    def set_word_wrap(self, enabled: bool):
        """Enable or disable word wrap.
        
        Args:
            enabled: Whether to enable word wrap
        """
        if enabled:
            self.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.setLineWrapMode(QTextEdit.NoWrap) 