"""
Control panel component for video playback controls.
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QSlider, 
                           QLabel)
from PyQt5.QtCore import Qt, pyqtSignal
from ...config.settings import POSITION_SLIDER_RANGE, DEFAULT_VOLUME, UI_TEXTS


class ControlPanel(QWidget):
    """Panel for video playback controls."""
    
    # Signals
    play_pause_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    position_changed = pyqtSignal(int)  # Position in slider units
    volume_changed = pyqtSignal(int)    # Volume (0-100)
    
    def __init__(self, parent=None):
        """Initialize the control panel.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the control panel UI."""
        layout = QHBoxLayout(self)
        
        # Play/Pause button
        self.play_button = QPushButton(UI_TEXTS['play_button'])
        self.play_button.clicked.connect(self._on_play_pause_clicked)
        layout.addWidget(self.play_button)
        
        # Stop button
        self.stop_button = QPushButton(UI_TEXTS['stop_button'])
        self.stop_button.clicked.connect(self._on_stop_clicked)
        layout.addWidget(self.stop_button)
        
        # Position slider
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, POSITION_SLIDER_RANGE)
        self.position_slider.setValue(0)
        self.position_slider.sliderMoved.connect(self._on_position_changed)
        layout.addWidget(self.position_slider)
        
        # Time label
        self.time_label = QLabel("00:00 / 00:00")
        layout.addWidget(self.time_label)
        
        # Volume label
        volume_label = QLabel(UI_TEXTS['volume_label'])
        layout.addWidget(volume_label)
        
        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(DEFAULT_VOLUME)
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        layout.addWidget(self.volume_slider)
        
        # Initially disable controls
        self.set_controls_enabled(False)
        
    def _on_play_pause_clicked(self):
        """Handle play/pause button click."""
        self.play_pause_requested.emit()
        
    def _on_stop_clicked(self):
        """Handle stop button click."""
        self.stop_requested.emit()
        
    def _on_position_changed(self, position: int):
        """Handle position slider change.
        
        Args:
            position: New position value
        """
        self.position_changed.emit(position)
        
    def _on_volume_changed(self, volume: int):
        """Handle volume slider change.
        
        Args:
            volume: New volume value
        """
        self.volume_changed.emit(volume)
        
    def set_play_button_text(self, text: str):
        """Set the play button text.
        
        Args:
            text: Button text
        """
        self.play_button.setText(text)
        
    def set_playing_state(self, is_playing: bool):
        """Set the playing state of the controls.
        
        Args:
            is_playing: Whether video is currently playing
        """
        if is_playing:
            self.play_button.setText(UI_TEXTS['pause_button'])
        else:
            self.play_button.setText(UI_TEXTS['play_button'])
            
    def set_position(self, position: int):
        """Set the position slider value.
        
        Args:
            position: Position value (0-1000)
        """
        # Temporarily disconnect signal to avoid feedback
        self.position_slider.blockSignals(True)
        self.position_slider.setValue(position)
        self.position_slider.blockSignals(False)
        
    def set_time_display(self, current_time: str, total_time: str):
        """Set the time display.
        
        Args:
            current_time: Current playback time
            total_time: Total video duration
        """
        self.time_label.setText(f"{current_time} / {total_time}")
        
    def set_volume(self, volume: int):
        """Set the volume slider value.
        
        Args:
            volume: Volume value (0-100)
        """
        # Temporarily disconnect signal to avoid feedback
        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(volume)
        self.volume_slider.blockSignals(False)
        
    def get_volume(self) -> int:
        """Get the current volume value.
        
        Returns:
            Volume value (0-100)
        """
        return self.volume_slider.value()
        
    def get_position(self) -> int:
        """Get the current position value.
        
        Returns:
            Position value (0-1000)
        """
        return self.position_slider.value()
        
    def set_controls_enabled(self, enabled: bool):
        """Enable or disable all controls.
        
        Args:
            enabled: Whether to enable controls
        """
        self.play_button.setEnabled(enabled)
        self.stop_button.setEnabled(enabled)
        self.position_slider.setEnabled(enabled)
        self.volume_slider.setEnabled(enabled)
        
    def set_position_slider_enabled(self, enabled: bool):
        """Enable or disable the position slider.
        
        Args:
            enabled: Whether to enable the position slider
        """
        self.position_slider.setEnabled(enabled)
        
    def reset_controls(self):
        """Reset all controls to initial state."""
        self.set_position(0)
        self.set_time_display("00:00", "00:00")
        self.set_playing_state(False)
        
    def set_position_range(self, maximum: int):
        """Set the maximum value for the position slider.
        
        Args:
            maximum: Maximum position value
        """
        self.position_slider.setMaximum(maximum)
        
    def is_position_slider_pressed(self) -> bool:
        """Check if the position slider is currently being pressed.
        
        Returns:
            True if slider is being pressed
        """
        return self.position_slider.isSliderDown() 