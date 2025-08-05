from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
import sys
import json
import os
from datetime import date

from screen_monitor import ScreenMonitor
from screen_break_timer import ScreenBreakTimer
from monitor_ui import Ui_MainWindow  # from your .ui file


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.break_timer = ScreenBreakTimer()

        # Connect UI buttons to functions (make sure these object names match .ui file!)
        self.ui.breakStartButton.clicked.connect(self.break_timer.start)
        self.ui.breakStopButton.clicked.connect(self.break_timer.stop)
        self.ui.monitorButton.clicked.connect(self.open_screen_monitor)
        self.ui.usageButton.clicked.connect(self.today_usage)

    def open_screen_monitor(self):
        self.monitor_window = ScreenMonitor()
        self.monitor_window.show()

    def today_usage(self):
        today = date.today().isoformat()
        file_path = os.path.join("Screen Care App", "data", f"app_usage_{today}.json")

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                usage_data = json.load(file)

            usage_summary = ""
            for app, seconds in usage_data.items():
                hrs = int(seconds // 3600)
                mins = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                usage_summary += f"{app}: {hrs:02d}:{mins:02d}:{secs:02d}\n"
            QMessageBox.information(self, "Today's Usage", usage_summary)
        else:
            QMessageBox.information(self, "No Data", "No usage data available for today.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec())
