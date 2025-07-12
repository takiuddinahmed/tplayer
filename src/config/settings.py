"""
Configuration settings for TPlayer application.
"""

# Application settings
APP_NAME = "TPlayer"
APP_VERSION = "1.0.0"
WINDOW_TITLE = "TPlayer - Video Player"

# Window settings
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
DEFAULT_WINDOW_X = 100
DEFAULT_WINDOW_Y = 100

# Video player settings
DEFAULT_VIDEO_WIDTH = 640
DEFAULT_VIDEO_HEIGHT = 480
DEFAULT_VOLUME = 50
POSITION_SLIDER_RANGE = 1000
TIMER_UPDATE_INTERVAL = 1000  # milliseconds

# File panel settings
FILE_PANEL_WIDTH = 300
DEBUG_CONSOLE_HEIGHT = 100

# Video file extensions
VIDEO_EXTENSIONS = [
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', 
    '.flv', '.webm', '.m4v', '.3gp'
]

# Network settings
REQUEST_TIMEOUT = 5  # seconds
DEFAULT_TEST_URL = "http://172.16.50.14/"
SAMPLE_VIDEO_URL = "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"

# UI Text
UI_TEXTS = {
    'file_panel_title': '🎬 Video Files',
    'browse_button': '📁 Browse Files',
    'scan_button': '🔍 Scan URL',
    'file_panel_instructions': 'Browse for local files or scan URLs for videos',
    'play_button': 'Play',
    'pause_button': 'Pause',
    'stop_button': 'Stop',
    'volume_label': 'Volume:',
    'url_label': 'URL:',
    'load_button': 'Load',
    'test_button': 'Test Sample Video',
    'url_placeholder': 'Enter video URL or directory URL',
    'no_videos_found': 'No videos found',
    'debug_console_title': 'TPlayer Debug Console'
}

# File dialog settings
FILE_DIALOG_FILTER = "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v *.3gp);;All Files (*)" 