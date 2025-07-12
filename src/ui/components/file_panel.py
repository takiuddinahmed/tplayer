"""
File panel component for browsing and managing video files.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, 
                           QListWidgetItem, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from typing import List, Dict, Optional
from ...config.settings import FILE_PANEL_WIDTH, UI_TEXTS


class FilePanel(QWidget):
    """Panel for browsing and managing video files."""
    
    # Signals
    file_selected = pyqtSignal(str)  # Emitted when a file is selected
    browse_requested = pyqtSignal()  # Emitted when browse button is clicked
    scan_requested = pyqtSignal()    # Emitted when scan button is clicked
    
    def __init__(self, parent=None):
        """Initialize the file panel.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the file panel UI."""
        self.setFixedWidth(FILE_PANEL_WIDTH)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(UI_TEXTS['file_panel_title'])
        title_label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(title_label)
        
        # File list
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.file_list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.file_list)
        
        # Browse button
        self.browse_button = QPushButton(UI_TEXTS['browse_button'])
        self.browse_button.clicked.connect(self._on_browse_clicked)
        layout.addWidget(self.browse_button)
        
        # Scan URL button
        self.scan_button = QPushButton(UI_TEXTS['scan_button'])
        self.scan_button.clicked.connect(self._on_scan_clicked)
        layout.addWidget(self.scan_button)
        
        # Instructions
        instructions = QLabel(UI_TEXTS['file_panel_instructions'])
        instructions.setWordWrap(True)
        instructions.setStyleSheet("font-size: 10px; color: gray; padding: 5px;")
        layout.addWidget(instructions)
        
    def _on_item_double_clicked(self, item: QListWidgetItem):
        """Handle double-click on file list item.
        
        Args:
            item: The clicked item
        """
        file_url = item.data(Qt.UserRole)
        if file_url:
            self.file_selected.emit(file_url)
            
    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle single-click on file list item.
        
        Args:
            item: The clicked item
        """
        # Could be used for preview or other actions
        pass
        
    def _on_browse_clicked(self):
        """Handle browse button click."""
        self.browse_requested.emit()
        
    def _on_scan_clicked(self):
        """Handle scan button click."""
        self.scan_requested.emit()
        
    def update_file_list(self, video_files: List[Dict[str, str]]):
        """Update the file list with new video files.
        
        Args:
            video_files: List of video file dictionaries
        """
        self.file_list.clear()
        
        if not video_files:
            item = QListWidgetItem(UI_TEXTS['no_videos_found'])
            item.setData(Qt.UserRole, None)
            self.file_list.addItem(item)
            return
            
        for video_file in video_files:
            display_name = video_file.get('name', 'Unknown')
            file_url = video_file.get('url', '')
            file_size = video_file.get('size', '')
            file_type = video_file.get('type', '')
            
            # Create display text
            if file_size:
                display_text = f"{display_name} ({file_size})"
            else:
                display_text = display_name
                
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, file_url)
            item.setToolTip(f"URL: {file_url}\nType: {file_type}")
            
            self.file_list.addItem(item)
            
    def add_file(self, video_file: Dict[str, str]):
        """Add a single file to the list.
        
        Args:
            video_file: Video file dictionary
        """
        # Remove "no videos found" item if it exists
        if self.file_list.count() == 1:
            first_item = self.file_list.item(0)
            if first_item and first_item.data(Qt.UserRole) is None:
                self.file_list.clear()
                
        display_name = video_file.get('name', 'Unknown')
        file_url = video_file.get('url', '')
        file_size = video_file.get('size', '')
        file_type = video_file.get('type', '')
        
        # Create display text
        if file_size:
            display_text = f"{display_name} ({file_size})"
        else:
            display_text = display_name
            
        item = QListWidgetItem(display_text)
        item.setData(Qt.UserRole, file_url)
        item.setToolTip(f"URL: {file_url}\nType: {file_type}")
        
        self.file_list.addItem(item)
        
    def clear_file_list(self):
        """Clear the file list."""
        self.file_list.clear()
        
    def get_selected_file(self) -> Optional[str]:
        """Get the currently selected file URL.
        
        Returns:
            Selected file URL or None if nothing is selected
        """
        current_item = self.file_list.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None
        
    def get_file_count(self) -> int:
        """Get the number of files in the list.
        
        Returns:
            Number of files
        """
        return self.file_list.count()
        
    def select_file_by_url(self, url: str):
        """Select a file by its URL.
        
        Args:
            url: URL of the file to select
        """
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item and item.data(Qt.UserRole) == url:
                self.file_list.setCurrentItem(item)
                break
                
    def set_browse_enabled(self, enabled: bool):
        """Enable or disable the browse button.
        
        Args:
            enabled: Whether to enable the button
        """
        self.browse_button.setEnabled(enabled)
        
    def set_scan_enabled(self, enabled: bool):
        """Enable or disable the scan button.
        
        Args:
            enabled: Whether to enable the button
        """
        self.scan_button.setEnabled(enabled) 