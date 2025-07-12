"""
Video widget component for displaying video content.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QBrush, QColor
from ...config.settings import DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT


class VideoWidget(QWidget):
    """Widget for displaying video content."""
    
    # Signals
    clicked = pyqtSignal()
    double_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize the video widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the video widget UI."""
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT)
        
        # Accept mouse events
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        
        # Set focus policy
        self.setFocusPolicy(Qt.StrongFocus)
        
    def paintEvent(self, event):
        """Paint event handler for custom drawing.
        
        Args:
            event: Paint event
        """
        painter = QPainter(self)
        
        # Fill with black background
        painter.fillRect(self.rect(), QBrush(QColor(0, 0, 0)))
        
        # If no video is playing, show a placeholder
        if not self.has_video():
            painter.setPen(QColor(128, 128, 128))
            painter.drawText(self.rect(), Qt.AlignCenter, "No video loaded")
            
    def mousePressEvent(self, event):
        """Mouse press event handler.
        
        Args:
            event: Mouse event
        """
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
        
    def mouseDoubleClickEvent(self, event):
        """Mouse double-click event handler.
        
        Args:
            event: Mouse event
        """
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)
        
    def has_video(self):
        """Check if video is currently loaded.
        
        Returns:
            True if video is loaded (this is a placeholder)
        """
        # This is a placeholder implementation
        # In a real application, you would check if VLC is actually playing
        return False
        
    def set_aspect_ratio(self, width: int, height: int):
        """Set the aspect ratio for the video widget.
        
        Args:
            width: Video width
            height: Video height
        """
        if height > 0:
            aspect_ratio = width / height
            current_width = self.width()
            new_height = int(current_width / aspect_ratio)
            self.setMinimumSize(current_width, new_height)
            
    def get_window_id(self):
        """Get the window ID for VLC integration.
        
        Returns:
            Window ID as integer
        """
        return int(self.winId())
        
    def reset(self):
        """Reset the video widget to initial state."""
        self.update()  # Trigger repaint 