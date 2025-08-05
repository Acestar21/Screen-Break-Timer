from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
import sys
import json
import os
from datetime import date
from screen_monitor import ScreenMonitor
from screen_break_timer import ScreenBreakTimer


def today_usage():
    today = date.today().isoformat()
    file_path = f"Screen Care App/data/app_usage_{today}.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            usage_data = json.load(file)

        usage_summary = ""
        for app, seconds in usage_data.items():
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            usage_summary += f"{app}: {hrs:02d}:{mins:02d}:{secs:02d}\n"
        QMessageBox.information(None, "Today's Usage", usage_summary)
    else:
        QMessageBox.information(None, "No Data", "No usage data available for today.")


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Care Assistant")
        self.setGeometry(100, 100, 600, 480)

        self.break_timer = ScreenBreakTimer()

        layout = QVBoxLayout()

        title = QLabel("Screen Care Assistant")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        self.break_start_button = QPushButton("Start Break Timer")
        self.break_stop_button = QPushButton("Stop Break Timer")
        layout.addWidget(self.break_start_button)
        layout.addWidget(self.break_stop_button)

        self.break_start_button.clicked.connect(self.break_timer.start)
        self.break_stop_button.clicked.connect(self.break_timer.stop)

        btn_3 = QPushButton("Screen Monitor")
        btn_3.clicked.connect(self.open_screen_monitor)
        layout.addWidget(btn_3)

        btn_5 = QPushButton("View Today Usage")
        btn_5.clicked.connect(today_usage)
        layout.addWidget(btn_5)

        self.setLayout(layout)

    def open_screen_monitor(self):
        self.monitor_window = ScreenMonitor()
        self.monitor_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec())
