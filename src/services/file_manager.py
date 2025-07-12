"""
File manager service for handling file operations.
"""

import os
from typing import List, Dict, Optional
from PyQt5.QtWidgets import QFileDialog, QWidget
from ..utils.logger import logger
from ..config.settings import VIDEO_EXTENSIONS, FILE_DIALOG_FILTER


class FileManager:
    """Service class for managing file operations."""
    
    def __init__(self):
        """Initialize the file manager."""
        self.last_directory = os.path.expanduser("~")
        
    def browse_for_video_file(self, parent: QWidget = None) -> Optional[str]:
        """Browse for a single video file.
        
        Args:
            parent: Parent widget for the dialog
            
        Returns:
            Selected file path or None if cancelled
        """
        try:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(
                parent,
                "Select Video File",
                self.last_directory,
                FILE_DIALOG_FILTER
            )
            
            if file_path:
                self.last_directory = os.path.dirname(file_path)
                logger.info(f"Selected file: {file_path}")
                return file_path
            else:
                logger.info("No file selected")
                return None
                
        except Exception as e:
            logger.error(f"Error browsing for file: {str(e)}")
            return None
            
    def browse_for_video_files(self, parent: QWidget = None) -> List[str]:
        """Browse for multiple video files.
        
        Args:
            parent: Parent widget for the dialog
            
        Returns:
            List of selected file paths
        """
        try:
            file_dialog = QFileDialog()
            file_paths, _ = file_dialog.getOpenFileNames(
                parent,
                "Select Video Files",
                self.last_directory,
                FILE_DIALOG_FILTER
            )
            
            if file_paths:
                self.last_directory = os.path.dirname(file_paths[0])
                logger.info(f"Selected {len(file_paths)} files")
                return file_paths
            else:
                logger.info("No files selected")
                return []
                
        except Exception as e:
            logger.error(f"Error browsing for files: {str(e)}")
            return []
            
    def browse_for_directory(self, parent: QWidget = None) -> Optional[str]:
        """Browse for a directory.
        
        Args:
            parent: Parent widget for the dialog
            
        Returns:
            Selected directory path or None if cancelled
        """
        try:
            file_dialog = QFileDialog()
            directory = file_dialog.getExistingDirectory(
                parent,
                "Select Directory",
                self.last_directory
            )
            
            if directory:
                self.last_directory = directory
                logger.info(f"Selected directory: {directory}")
                return directory
            else:
                logger.info("No directory selected")
                return None
                
        except Exception as e:
            logger.error(f"Error browsing for directory: {str(e)}")
            return None
            
    def get_video_files_in_directory(self, directory: str) -> List[Dict[str, str]]:
        """Get all video files in a directory.
        
        Args:
            directory: Directory path to search
            
        Returns:
            List of dictionaries containing video file information
        """
        video_files = []
        
        try:
            if not os.path.exists(directory):
                logger.error(f"Directory does not exist: {directory}")
                return video_files
                
            logger.info(f"Scanning directory for videos: {directory}")
            
            for filename in os.listdir(directory):
                if self._is_video_file(filename):
                    file_path = os.path.join(directory, filename)
                    
                    try:
                        file_info = self._get_file_info(file_path)
                        video_files.append(file_info)
                    except Exception as e:
                        logger.error(f"Error processing file {filename}: {str(e)}")
                        continue
                        
            logger.info(f"Found {len(video_files)} video files in directory")
            return video_files
            
        except Exception as e:
            logger.error(f"Error scanning directory: {str(e)}")
            return video_files
            
    def _is_video_file(self, filename: str) -> bool:
        """Check if a filename is a video file.
        
        Args:
            filename: Filename to check
            
        Returns:
            True if it's a video file, False otherwise
        """
        filename_lower = filename.lower()
        return any(filename_lower.endswith(ext) for ext in VIDEO_EXTENSIONS)
        
    def _get_file_info(self, file_path: str) -> Dict[str, str]:
        """Get file information.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file information
        """
        try:
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_size_str = self._format_file_size(file_size)
            
            return {
                'name': filename,
                'path': file_path,
                'url': f"file://{file_path}",
                'size': file_size_str,
                'type': self._get_video_type(filename)
            }
            
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'url': f"file://{file_path}",
                'size': 'Unknown',
                'type': 'VIDEO'
            }
            
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
        
    def _get_video_type(self, filename: str) -> str:
        """Get video type from filename.
        
        Args:
            filename: Filename to analyze
            
        Returns:
            Video type/extension
        """
        try:
            return filename.split('.')[-1].upper()
        except Exception:
            return "VIDEO"
            
    def is_valid_video_file(self, file_path: str) -> bool:
        """Check if a file path is a valid video file.
        
        Args:
            file_path: File path to check
            
        Returns:
            True if it's a valid video file, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False
                
            if not os.path.isfile(file_path):
                return False
                
            filename = os.path.basename(file_path)
            return self._is_video_file(filename)
            
        except Exception as e:
            logger.error(f"Error checking file validity: {str(e)}")
            return False
            
    def get_recent_files(self, max_files: int = 10) -> List[str]:
        """Get list of recently accessed files.
        
        Args:
            max_files: Maximum number of files to return
            
        Returns:
            List of recently accessed file paths
        """
        # This is a placeholder implementation
        # In a real application, you would maintain a list of recent files
        # possibly stored in a config file or database
        return []
        
    def add_to_recent_files(self, file_path: str):
        """Add a file to the recent files list.
        
        Args:
            file_path: File path to add
        """
        # This is a placeholder implementation
        # In a real application, you would add the file to your recent files list
        logger.info(f"Added to recent files: {file_path}")
        
    def cleanup(self):
        """Clean up resources."""
        # No cleanup needed for this service
        logger.info("File manager cleaned up") 