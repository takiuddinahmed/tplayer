# TPlayer - Organized Video Player Application

A Python-based video player application built with PyQt5 and VLC. This application has been refactored from a monolithic structure into a well-organized, modular architecture.

## 🏗️ Architecture Overview

The application has been completely reorganized into the following structure:

```
TPlayer/
├── src/
│   ├── main.py                 # Main application entry point
│   ├── ui/
│   │   ├── main_window.py      # Main window orchestrating all components
│   │   └── components/
│   │       ├── video_widget.py      # Video display widget
│   │       ├── file_panel.py        # File browsing panel
│   │       ├── control_panel.py     # Video playback controls
│   │       ├── url_input.py         # URL input component
│   │       └── debug_console.py     # Debug message console
│   ├── services/
│   │   ├── video_service.py    # VLC video playback service
│   │   ├── url_scanner.py      # URL scanning and video extraction
│   │   └── file_manager.py     # File operations and management
│   ├── utils/
│   │   ├── logger.py           # Logging utility
│   │   └── time_formatter.py   # Time formatting functions
│   └── config/
│       └── settings.py         # Application configuration
├── main.py                     # Legacy entry point (now uses organized structure)
└── pyproject.toml             # Project dependencies
```

## 🎯 Features

- **Video Playback**: Play various video formats using VLC backend
- **File Browsing**: Browse and select local video files
- **URL Support**: Load videos from URLs or scan web directories
- **Playback Controls**: Play, pause, stop, seek, and volume control
- **Debug Console**: Real-time logging and debugging information
- **Modular Design**: Clean separation of concerns with reusable components

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- PyQt5
- VLC Media Player installed on your system
- python-vlc package

### Installation

1. **Install VLC Media Player** (if not already installed):
   - **macOS**: `brew install vlc`
   - **Ubuntu/Debian**: `sudo apt-get install vlc`
   - **Windows**: Download from [VLC website](https://www.videolan.org/vlc/)

2. **Install Python dependencies**:
   ```bash
   pip install PyQt5 python-vlc requests
   ```

### Running the Application

```bash
python main.py
```

## 📁 Component Details

### Services Layer

**VideoService** (`src/services/video_service.py`)
- Manages VLC media player operations
- Handles video loading, playback control, and state management
- Provides callbacks for UI updates

**URLScanner** (`src/services/url_scanner.py`)
- Scans web pages for video file links
- Extracts file information (size, type)
- Supports various video formats

**FileManager** (`src/services/file_manager.py`)
- Handles local file operations
- Manages file dialogs and directory scanning
- Validates video file formats

### UI Components

**MainWindow** (`src/ui/main_window.py`)
- Orchestrates all UI components and services
- Manages application lifecycle and cleanup
- Handles signal connections between components

**VideoWidget** (`src/ui/components/video_widget.py`)
- Custom widget for video display
- Handles mouse events for play/pause
- Provides VLC integration interface

**FilePanel** (`src/ui/components/file_panel.py`)
- File browsing and selection interface
- Displays video files with metadata
- Emits signals for file operations

**ControlPanel** (`src/ui/components/control_panel.py`)
- Video playback controls (play, pause, stop)
- Position slider and time display
- Volume control

**URLInput** (`src/ui/components/url_input.py`)
- URL input field with validation
- Load and test video functionality
- Keyboard shortcuts support

**DebugConsole** (`src/ui/components/debug_console.py`)
- Real-time logging display
- Formatted message types (info, error, warning)
- Scrollable history with auto-scroll

### Utilities

**Logger** (`src/utils/logger.py`)
- Centralized logging system
- Supports console and GUI output
- Configurable log levels

**TimeFormatter** (`src/utils/time_formatter.py`)
- Time formatting utilities
- Supports MM:SS and HH:MM:SS formats
- Handles invalid time values

### Configuration

**Settings** (`src/config/settings.py`)
- Application-wide configuration
- UI constants and defaults
- File extensions and network settings

## 🔧 Usage

### Basic Video Playback

1. **Load Local File**: Click "📁 Browse Files" to select a video file
2. **Load from URL**: Enter a video URL and click "Load"
3. **Scan Directory**: Enter a directory URL and click "🔍 Scan URL"
4. **Test Sample**: Click "Test Sample Video" to load a sample video

### Playback Controls

- **Play/Pause**: Click the play button or click on the video
- **Stop**: Click the stop button
- **Seek**: Drag the position slider
- **Volume**: Adjust the volume slider
- **Fullscreen**: Double-click the video widget

### Supported Formats

- MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V, 3GP
- Any format supported by VLC Media Player

## 🛠️ Development

### Adding New Components

1. Create the component in `src/ui/components/`
2. Inherit from appropriate Qt widget
3. Implement signal-slot pattern for communication
4. Add to main window and connect signals

### Adding New Services

1. Create service in `src/services/`
2. Implement initialization and cleanup methods
3. Add error handling and logging
4. Integrate with main window

### Configuration

Modify `src/config/settings.py` to add new configuration options.

## 🏆 Benefits of the New Architecture

### 🎯 Separation of Concerns
- **UI Components**: Handle only presentation logic
- **Services**: Manage business logic and external integrations
- **Utilities**: Provide reusable functionality
- **Configuration**: Centralize application settings

### 🔧 Maintainability
- **Modular Design**: Easy to locate and modify specific functionality
- **Single Responsibility**: Each class has a clear, focused purpose
- **Loose Coupling**: Components communicate through well-defined interfaces

### 🧪 Testability
- **Isolated Components**: Services can be tested independently
- **Dependency Injection**: Easy to mock services for testing
- **Clear Interfaces**: Predictable input/output behavior

### 📈 Scalability
- **Extensible**: Easy to add new features and components
- **Reusable**: Components can be reused in other projects
- **Configurable**: Behavior can be modified without code changes

## 🐛 Debugging

The application includes a built-in debug console that displays:
- Application initialization status
- Video loading progress
- Error messages and warnings
- Network requests and responses

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the established architecture
4. Add tests for new functionality
5. Submit a pull request

## 🆘 Troubleshooting

### VLC Not Found
- Ensure VLC Media Player is installed
- Check that `python-vlc` package is installed
- Verify VLC is in your system PATH

### Video Not Playing
- Check video format compatibility
- Verify file/URL accessibility
- Check debug console for error messages

### Performance Issues
- Close other applications using video resources
- Check available system memory
- Try reducing video resolution

---

*This application demonstrates best practices in Python GUI development with clean architecture, proper separation of concerns, and maintainable code structure.*
