"""
Logger utility for TPlayer application.
"""

import logging
from typing import Optional


class TPlayerLogger:
    """Logger utility class for TPlayer application."""
    
    def __init__(self, name: str = "TPlayer", level: int = logging.INFO):
        """Initialize the logger.
        
        Args:
            name: Logger name
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Avoid adding handlers if they already exist
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
        self.debug_callback: Optional[callable] = None
        
    def set_debug_callback(self, callback: callable):
        """Set callback function for debug messages.
        
        Args:
            callback: Function to call with debug messages
        """
        self.debug_callback = callback
        
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
        if self.debug_callback:
            self.debug_callback(message)
            
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
        if self.debug_callback:
            self.debug_callback(message)
            
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
        if self.debug_callback:
            self.debug_callback(message)
            
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
        if self.debug_callback:
            self.debug_callback(f"ERROR: {message}")
            
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)
        if self.debug_callback:
            self.debug_callback(f"CRITICAL: {message}")


# Global logger instance
logger = TPlayerLogger() 