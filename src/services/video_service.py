"""
Video service for managing VLC player operations.
"""

import sys
import vlc
from typing import Optional, Callable
from ..utils.logger import logger
from ..utils.time_formatter import format_time
from ..config.settings import DEFAULT_VOLUME


class VideoService:
    """Service class for managing video playback using VLC."""
    
    def __init__(self):
        """Initialize the video service."""
        self.vlc_instance: Optional[vlc.Instance] = None
        self.vlc_player: Optional[vlc.MediaPlayer] = None
        self.is_initialized = False
        self.initialization_error: Optional[str] = None
        
        # Callbacks
        self.on_position_change: Optional[Callable[[float], None]] = None
        self.on_time_change: Optional[Callable[[int, int], None]] = None
        self.on_state_change: Optional[Callable[[str], None]] = None
        
        self._initialize_vlc()
        
    def _initialize_vlc(self):
        """Initialize VLC instance and player."""
        try:
            self.vlc_instance = vlc.Instance()
            self.vlc_player = self.vlc_instance.media_player_new()
            
            # Set default volume
            self.vlc_player.audio_set_volume(DEFAULT_VOLUME)
            
            self.is_initialized = True
            logger.info("VLC initialized successfully")
            
        except Exception as e:
            self.initialization_error = str(e)
            logger.error(f"VLC initialization failed: {self.initialization_error}")
            self.is_initialized = False
            
    def set_video_widget(self, widget):
        """Set the video widget for displaying video.
        
        Args:
            widget: Qt widget to display video in
        """
        if not self.is_initialized:
            logger.error("VLC not initialized")
            return False
            
        try:
            if sys.platform == "darwin":  # macOS
                self.vlc_player.set_nsobject(int(widget.winId()))
            else:  # Linux/Windows
                self.vlc_player.set_hwnd(int(widget.winId()))
                
            logger.info("Video widget set successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set video widget: {str(e)}")
            return False
            
    def load_media(self, url: str) -> bool:
        """Load media from URL or file path.
        
        Args:
            url: URL or file path to load
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_initialized:
            logger.error("VLC not initialized")
            return False
            
        try:
            media = self.vlc_instance.media_new(url)
            self.vlc_player.set_media(media)
            logger.info(f"Media loaded: {url}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load media: {str(e)}")
            return False
            
    def play(self) -> bool:
        """Start video playback.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_initialized:
            logger.error("VLC not initialized")
            return False
            
        try:
            result = self.vlc_player.play()
            if result == 0:
                logger.info("Video playback started")
                if self.on_state_change:
                    self.on_state_change("playing")
                return True
            else:
                logger.error(f"Failed to start playback, result: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to start playback: {str(e)}")
            return False
            
    def pause(self):
        """Pause video playback."""
        if not self.is_initialized:
            logger.error("VLC not initialized")
            return
            
        try:
            self.vlc_player.pause()
            logger.info("Video playback paused")
            if self.on_state_change:
                self.on_state_change("paused")
                
        except Exception as e:
            logger.error(f"Failed to pause playback: {str(e)}")
            
    def stop(self):
        """Stop video playback."""
        if not self.is_initialized:
            logger.error("VLC not initialized")
            return
            
        try:
            self.vlc_player.stop()
            logger.info("Video playback stopped")
            if self.on_state_change:
                self.on_state_change("stopped")
                
        except Exception as e:
            logger.error(f"Failed to stop playback: {str(e)}")
            
    def is_playing(self) -> bool:
        """Check if video is currently playing.
        
        Returns:
            True if playing, False otherwise
        """
        if not self.is_initialized:
            return False
            
        try:
            return self.vlc_player.is_playing()
        except Exception as e:
            logger.error(f"Failed to check playing state: {str(e)}")
            return False
            
    def set_position(self, position: float):
        """Set video position.
        
        Args:
            position: Position as float between 0.0 and 1.0
        """
        if not self.is_initialized:
            logger.error("VLC not initialized")
            return
            
        try:
            if self.vlc_player.get_media():
                self.vlc_player.set_position(position)
                
        except Exception as e:
            logger.error(f"Failed to set position: {str(e)}")
            
    def get_position(self) -> float:
        """Get current video position.
        
        Returns:
            Position as float between 0.0 and 1.0
        """
        if not self.is_initialized:
            return 0.0
            
        try:
            if self.vlc_player.get_media():
                return self.vlc_player.get_position()
            return 0.0
            
        except Exception as e:
            logger.error(f"Failed to get position: {str(e)}")
            return 0.0
            
    def set_volume(self, volume: int):
        """Set audio volume.
        
        Args:
            volume: Volume level (0-100)
        """
        if not self.is_initialized:
            logger.error("VLC not initialized")
            return
            
        try:
            self.vlc_player.audio_set_volume(volume)
            
        except Exception as e:
            logger.error(f"Failed to set volume: {str(e)}")
            
    def get_volume(self) -> int:
        """Get current audio volume.
        
        Returns:
            Volume level (0-100)
        """
        if not self.is_initialized:
            return 0
            
        try:
            return self.vlc_player.audio_get_volume()
        except Exception as e:
            logger.error(f"Failed to get volume: {str(e)}")
            return 0
            
    def get_time(self) -> int:
        """Get current playback time in milliseconds.
        
        Returns:
            Current time in milliseconds
        """
        if not self.is_initialized:
            return -1
            
        try:
            if self.vlc_player.get_media():
                return self.vlc_player.get_time()
            return -1
            
        except Exception as e:
            logger.error(f"Failed to get time: {str(e)}")
            return -1
            
    def get_length(self) -> int:
        """Get total media length in milliseconds.
        
        Returns:
            Total length in milliseconds
        """
        if not self.is_initialized:
            return -1
            
        try:
            if self.vlc_player.get_media():
                return self.vlc_player.get_length()
            return -1
            
        except Exception as e:
            logger.error(f"Failed to get length: {str(e)}")
            return -1
            
    def get_time_info(self) -> tuple:
        """Get formatted time information.
        
        Returns:
            Tuple of (current_time_str, total_time_str)
        """
        current_time = self.get_time()
        total_time = self.get_length()
        
        if current_time != -1 and total_time != -1:
            current_str = format_time(current_time)
            total_str = format_time(total_time)
            return (current_str, total_str)
        else:
            return ("00:00", "00:00")
            
    def update_callbacks(self):
        """Update callbacks with current state."""
        if not self.is_initialized:
            return
            
        # Update position callback
        if self.on_position_change:
            position = self.get_position()
            self.on_position_change(position)
            
        # Update time callback
        if self.on_time_change:
            current_time = self.get_time()
            total_time = self.get_length()
            if current_time != -1 and total_time != -1:
                self.on_time_change(current_time, total_time)
                
    def cleanup(self):
        """Clean up VLC resources."""
        if self.vlc_player:
            try:
                self.vlc_player.stop()
                logger.info("VLC player cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up VLC player: {str(e)}")
                
        self.vlc_player = None
        self.vlc_instance = None
        self.is_initialized = False 