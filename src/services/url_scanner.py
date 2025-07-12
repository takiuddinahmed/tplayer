"""
URL scanner service for extracting video links from web pages.
"""

import re
import requests
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from ..utils.logger import logger
from ..config.settings import VIDEO_EXTENSIONS, REQUEST_TIMEOUT


class URLScanner:
    """Service class for scanning URLs and extracting video links."""
    
    def __init__(self):
        """Initialize the URL scanner."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def scan_url_for_videos(self, url: str) -> List[Dict[str, str]]:
        """Scan URL for video files.
        
        Args:
            url: URL to scan
            
        Returns:
            List of dictionaries containing video file information
        """
        try:
            logger.info(f"Scanning URL for videos: {url}")
            
            # Get page content
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            page_content = response.text
            
            # Extract video links
            video_files = self._extract_video_links(page_content, url)
            
            logger.info(f"Found {len(video_files)} video files")
            return video_files
            
        except requests.RequestException as e:
            logger.error(f"Request error while scanning URL: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error scanning URL: {str(e)}")
            return []
            
    def _extract_video_links(self, html_content: str, base_url: str) -> List[Dict[str, str]]:
        """Extract video file links from HTML content.
        
        Args:
            html_content: HTML content to parse
            base_url: Base URL for resolving relative links
            
        Returns:
            List of dictionaries containing video file information
        """
        video_files = []
        
        # Find all href links
        href_pattern = r'href=["\']([^"\']+)["\']'
        matches = re.findall(href_pattern, html_content, re.IGNORECASE)
        
        for match in matches:
            if self._is_video_link(match):
                try:
                    # Convert to absolute URL
                    full_url = urljoin(base_url, match)
                    
                    # Extract filename for display
                    filename = self._extract_filename(match)
                    
                    # Get file size if possible
                    file_size = self._get_file_size(full_url)
                    
                    video_files.append({
                        'name': filename,
                        'url': full_url,
                        'size': file_size,
                        'type': self._get_video_type(filename)
                    })
                    
                except Exception as e:
                    logger.error(f"Error processing video link: {str(e)}")
                    continue
                    
        return video_files
        
    def _is_video_link(self, link: str) -> bool:
        """Check if a link points to a video file.
        
        Args:
            link: Link to check
            
        Returns:
            True if it's a video link, False otherwise
        """
        link_lower = link.lower()
        return any(link_lower.endswith(ext) for ext in VIDEO_EXTENSIONS)
        
    def _extract_filename(self, link: str) -> str:
        """Extract filename from a link.
        
        Args:
            link: Link to extract filename from
            
        Returns:
            Extracted filename
        """
        try:
            parsed_url = urlparse(link)
            filename = parsed_url.path.split('/')[-1]
            return filename if filename else link
        except Exception:
            return link
            
    def _get_file_size(self, url: str) -> Optional[str]:
        """Get file size from URL using HEAD request.
        
        Args:
            url: URL to check
            
        Returns:
            File size as formatted string or None if not available
        """
        try:
            response = self.session.head(url, timeout=REQUEST_TIMEOUT)
            content_length = response.headers.get('content-length')
            
            if content_length:
                size_bytes = int(content_length)
                return self._format_file_size(size_bytes)
                
        except Exception as e:
            logger.debug(f"Could not get file size for {url}: {str(e)}")
            
        return None
        
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
            
    def is_video_url(self, url: str) -> bool:
        """Check if URL is a direct video file.
        
        Args:
            url: URL to check
            
        Returns:
            True if it's a video URL, False otherwise
        """
        url_lower = url.lower()
        
        logger.debug(f"Checking if URL is video: {url}")
        
        # Check by extension first (most reliable)
        if any(url_lower.endswith(ext) for ext in VIDEO_EXTENSIONS):
            logger.debug(f"Video detected by extension: {url}")
            return True
            
        # Check by content type (for URLs without extensions)
        try:
            logger.debug(f"Checking content type for: {url}")
            response = self.session.head(url, timeout=REQUEST_TIMEOUT)
            content_type = response.headers.get('content-type', '').lower()
            logger.debug(f"Content type: {content_type}")
            
            if content_type.startswith('video/'):
                logger.debug(f"Video detected by content type: {url}")
                return True
                
        except Exception as e:
            logger.debug(f"Error checking content type: {str(e)}")
            
        logger.debug(f"Not a video URL: {url}")
        return False
        
    def get_video_info(self, url: str) -> Optional[Dict[str, str]]:
        """Get video information from URL.
        
        Args:
            url: Video URL
            
        Returns:
            Dictionary with video information or None if not available
        """
        try:
            response = self.session.head(url, timeout=REQUEST_TIMEOUT)
            
            filename = self._extract_filename(url)
            content_length = response.headers.get('content-length')
            content_type = response.headers.get('content-type', '')
            
            info = {
                'name': filename,
                'url': url,
                'type': self._get_video_type(filename),
                'content_type': content_type
            }
            
            if content_length:
                info['size'] = self._format_file_size(int(content_length))
                
            return info
            
        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            return None
            
    def cleanup(self):
        """Clean up resources."""
        if self.session:
            self.session.close()
            logger.info("URL scanner session closed") 