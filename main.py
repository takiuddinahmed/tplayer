"""
TPlayer - A Python video player application.

This is the main entry point that uses the organized code structure.
The original monolithic code has been refactored into:
- Services (video_service, url_scanner, file_manager)
- UI Components (video_widget, file_panel, control_panel, etc.)
- Utilities (logger, time_formatter)
- Configuration (settings)

To run the application, execute this file.
"""

import sys
import logging
from src.main import main

# Set up basic logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    sys.exit(main())
