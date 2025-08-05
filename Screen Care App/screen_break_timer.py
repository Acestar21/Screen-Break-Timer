from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt

class BreakPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Break Reminder")
        self.setGeometry(600, 300, 300, 150)

        layout = QVBoxLayout()
        label = QLabel("LOOK AWAY! (2 seconds)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

        # Auto-close popup after 2 seconds
        QTimer.singleShot(2000, self.close)

class ScreenBreakTimer:
    def __init__(self, parent=None):
        self.parent = parent
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_popup)

    def start(self):
        self.timer.start(5 * 1000)   # Trigger every 20 minutes
        print("Break timer started.")

    def stop(self):
        self.timer.stop()
        print("Break timer stopped.")

    def show_popup(self):
        self.popup = BreakPopup()
        if self.parent:
            self.popup.setParent(self.parent, Qt.WindowType.Dialog)
        self.popup.show()
