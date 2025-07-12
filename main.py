import sys
import platform
import vlc
from PyQt5 import QtWidgets, QtCore

class VideoPlayer(QtWidgets.QMainWindow):
    def __init__(self, video_url):
        super().__init__()
        self.setWindowTitle("VLC Streaming Player")
        self.resize(800, 450)

        # VLC setup with macOS compatibility options
        if platform.system() == "Darwin":  # macOS
            self.instance = vlc.Instance("--no-xlib", "--quiet")
        else:
            self.instance = vlc.Instance("--quiet")
        self.player = self.instance.media_player_new()

        # Qt Frame for video
        self.video_frame = QtWidgets.QFrame(self)
        self.setCentralWidget(self.video_frame)
        win_id = int(self.video_frame.winId())
        
        # Set the window handle based on platform
        if platform.system() == "Darwin":  # macOS
            self.player.set_nsobject(win_id)
        elif platform.system() == "Windows":
            self.player.set_hwnd(win_id)
        else:  # Linux/X11
            self.player.set_xwindow(win_id)

        # Direct VLC streaming - no download needed
        media = self.instance.media_new(video_url)
        self.player.set_media(media)
        self.player.play()
        
        # Enable focus for keyboard events
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts for video control"""
        key = event.key()
        
        if key == QtCore.Qt.Key_Left:
            # Seek backward 10 seconds
            current_time = self.player.get_time()
            new_time = max(0, current_time - 10000)  # VLC time is in milliseconds
            self.player.set_time(new_time)
            
        elif key == QtCore.Qt.Key_Right:
            # Seek forward 10 seconds
            current_time = self.player.get_time()
            new_time = current_time + 10000  # VLC time is in milliseconds
            self.player.set_time(new_time)
            
        elif key == QtCore.Qt.Key_Space:
            # Play/Pause toggle
            if self.player.is_playing():
                self.player.pause()
            else:
                self.player.play()
                
        elif key == QtCore.Qt.Key_Up:
            # Volume up
            current_volume = self.player.audio_get_volume()
            new_volume = min(100, current_volume + 10)
            self.player.audio_set_volume(new_volume)
            
        elif key == QtCore.Qt.Key_Down:
            # Volume down
            current_volume = self.player.audio_get_volume()
            new_volume = max(0, current_volume - 10)
            self.player.audio_set_volume(new_volume)
            
        elif key == QtCore.Qt.Key_M:
            # Mute/Unmute toggle
            self.player.audio_toggle_mute()
            
        elif key == QtCore.Qt.Key_F:
            # Toggle fullscreen
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
                
        else:
            # Pass other keys to parent
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    url = "http://172.16.50.14/DHAKA-FLIX-14/KOREAN%20TV%20%26%20WEB%20Series/Guardian-The%20Lonely%20and%20Great%20God%20%28Goblin%29%20%28TV%20Series%202016%E2%80%932017%29%201080p%20%5BDual%20Audio%5D/Season%201/Goblin%20S01E07%20%201080p%20NF%20WEBRip%20x265%20HEVC%20MSubs%20%5BDual%20Audio%5D%5BHindi%202.0%2BKorean%202.0%5D%20-MsHeist.mkv"
    player = VideoPlayer(url)
    player.show()
    sys.exit(app.exec_())
