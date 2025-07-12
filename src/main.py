"""
Main entry point for the TPlayer application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from .ui.main_window import MainWindow
from .config.settings import APP_NAME, APP_VERSION


def main():
    """Main entry point for the TPlayer application."""
    # Create QApplication instance
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Run the application
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main()) 