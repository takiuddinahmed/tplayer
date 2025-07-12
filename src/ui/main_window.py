"""
Main window for the TPlayer application.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QMessageBox, QApplication)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

from .components.video_widget import VideoWidget
from .components.file_panel import FilePanel
from .components.control_panel import ControlPanel
from .components.url_input import URLInput
from .components.debug_console import DebugConsole

from ..services.video_service import VideoService
from ..services.url_scanner import URLScanner
from ..services.file_manager import FileManager

from ..utils.logger import logger
from ..config.settings import (
    WINDOW_TITLE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_X, DEFAULT_WINDOW_Y, TIMER_UPDATE_INTERVAL
)


class MainWindow(QMainWindow):
    """Main window for the TPlayer application."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Initialize services
        self.video_service = VideoService()
        self.url_scanner = URLScanner()
        self.file_manager = FileManager()
        
        # Initialize UI
        self.setup_ui()
        self.setup_connections()
        self.setup_logger()
        self.setup_timer()
        
        # Log initialization status
        self.log_initialization_status()
        
    def setup_ui(self):
        """Set up the main window UI."""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(DEFAULT_WINDOW_X, DEFAULT_WINDOW_Y, 
                        DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create horizontal layout for video player and file list
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Create video widget
        self.video_widget = VideoWidget()
        content_layout.addWidget(self.video_widget)
        
        # Create file panel
        self.file_panel = FilePanel()
        content_layout.addWidget(self.file_panel)
        
        # Create control panel
        self.control_panel = ControlPanel()
        main_layout.addWidget(self.control_panel)
        
        # Create URL input
        self.url_input = URLInput()
        main_layout.addWidget(self.url_input)
        
        # Create debug console
        self.debug_console = DebugConsole()
        main_layout.addWidget(self.debug_console)
        
    def setup_connections(self):
        """Set up signal connections between components."""
        # File panel connections
        self.file_panel.file_selected.connect(self.load_video)
        self.file_panel.browse_requested.connect(self.browse_files)
        self.file_panel.scan_requested.connect(self.scan_url_for_videos)
        
        # Control panel connections
        self.control_panel.play_pause_requested.connect(self.toggle_play_pause)
        self.control_panel.stop_requested.connect(self.stop_video)
        self.control_panel.position_changed.connect(self.set_video_position)
        self.control_panel.volume_changed.connect(self.set_volume)
        
        # URL input connections
        self.url_input.url_load_requested.connect(self.load_from_url)
        self.url_input.test_video_requested.connect(self.load_video)
        
        # Video widget connections
        self.video_widget.clicked.connect(self.toggle_play_pause)
        self.video_widget.double_clicked.connect(self.toggle_fullscreen)
        
        # Video service callbacks
        self.video_service.on_state_change = self.on_video_state_change
        
    def setup_logger(self):
        """Set up logger to output to debug console."""
        logger.set_debug_callback(self.debug_console.append_message)
        
    def setup_timer(self):
        """Set up timer for updating video position."""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_video_position)
        
    def log_initialization_status(self):
        """Log the initialization status of services."""
        if self.video_service.is_initialized:
            logger.info("Video service initialized successfully")
        else:
            logger.error(f"Video service initialization failed: {self.video_service.initialization_error}")
            
        logger.info("Application initialized successfully")
        
    def browse_files(self):
        """Handle file browsing request."""
        file_path = self.file_manager.browse_for_video_file(self)
        if file_path:
            self.load_video(file_path)
            
    def scan_url_for_videos(self):
        """Handle URL scanning request."""
        url = self.url_input.get_url()
        if not url:
            logger.error("No URL entered")
            return
            
        logger.info(f"Scanning URL for videos: {url}")
        
        # Scan for videos
        video_files = self.url_scanner.scan_url_for_videos(url)
        
        # Update file panel
        self.file_panel.update_file_list(video_files)
        
    def load_from_url(self, url: str):
        """Handle URL load request.
        
        Args:
            url: URL to load
        """
        if self.url_scanner.is_video_url(url):
            self.load_video(url)
        else:
            # Try to scan for videos
            self.scan_url_for_videos()
            
    def load_video(self, url: str):
        """Load and play video.
        
        Args:
            url: Video URL or file path
        """
        if not self.video_service.is_initialized:
            error_msg = "Video service not initialized"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            return
            
        try:
            logger.info(f"Loading video: {url}")
            
            # Set video widget for VLC
            if not self.video_service.set_video_widget(self.video_widget):
                logger.error("Failed to set video widget")
                return
                
            # Load media
            if not self.video_service.load_media(url):
                logger.error("Failed to load media")
                return
                
            # Start playback
            if self.video_service.play():
                # Start update timer
                self.update_timer.start(TIMER_UPDATE_INTERVAL)
                
                # Enable controls
                self.control_panel.set_controls_enabled(True)
                
                # Update window title
                filename = url.split('/')[-1]
                self.setWindowTitle(f"{WINDOW_TITLE} - Playing: {filename}")
                
                logger.info("Video loaded and playback started successfully")
            else:
                logger.error("Failed to start video playback")
                
        except Exception as e:
            error_msg = f"Failed to load video: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            
    def toggle_play_pause(self):
        """Toggle play/pause for video."""
        if not self.video_service.is_initialized:
            return
            
        if self.video_service.is_playing():
            self.video_service.pause()
        else:
            self.video_service.play()
            
    def stop_video(self):
        """Stop video playback."""
        if not self.video_service.is_initialized:
            return
            
        self.video_service.stop()
        self.update_timer.stop()
        
        # Reset controls
        self.control_panel.reset_controls()
        
        # Reset window title
        self.setWindowTitle(WINDOW_TITLE)
        
        logger.info("Video playback stopped")
        
    def set_video_position(self, position: int):
        """Set video position from slider.
        
        Args:
            position: Position in slider units (0-1000)
        """
        if self.video_service.is_initialized:
            normalized_position = position / 1000.0
            self.video_service.set_position(normalized_position)
            
    def set_volume(self, volume: int):
        """Set video volume.
        
        Args:
            volume: Volume level (0-100)
        """
        if self.video_service.is_initialized:
            self.video_service.set_volume(volume)
            
    def update_video_position(self):
        """Update video position slider and time display."""
        if not self.video_service.is_initialized:
            return
            
        # Don't update if user is dragging the slider
        if self.control_panel.is_position_slider_pressed():
            return
            
        # Update position
        position = self.video_service.get_position()
        position_slider_value = int(position * 1000)
        self.control_panel.set_position(position_slider_value)
        
        # Update time display
        current_time_str, total_time_str = self.video_service.get_time_info()
        self.control_panel.set_time_display(current_time_str, total_time_str)
        
    def on_video_state_change(self, state: str):
        """Handle video state changes.
        
        Args:
            state: New video state
        """
        if state == "playing":
            self.control_panel.set_playing_state(True)
        elif state in ["paused", "stopped"]:
            self.control_panel.set_playing_state(False)
            
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def closeEvent(self, event):
        """Handle window close event.
        
        Args:
            event: Close event
        """
        # Clean up services
        self.video_service.cleanup()
        self.url_scanner.cleanup()
        self.file_manager.cleanup()
        
        # Stop timer
        if self.update_timer.isActive():
            self.update_timer.stop()
            
        logger.info("Application closing")
        event.accept()
        
    def show_about(self):
        """Show about dialog."""
        about_text = f"""
        <h3>{WINDOW_TITLE}</h3>
        <p>A Python-based video player application.</p>
        <p>Built with PyQt5 and VLC.</p>
        """
        QMessageBox.about(self, "About TPlayer", about_text)
        
    def show_error(self, title: str, message: str):
        """Show error dialog.
        
        Args:
            title: Dialog title
            message: Error message
        """
        QMessageBox.critical(self, title, message)
        
    def show_info(self, title: str, message: str):
        """Show info dialog.
        
        Args:
            title: Dialog title
            message: Info message
        """
        QMessageBox.information(self, title, message) 