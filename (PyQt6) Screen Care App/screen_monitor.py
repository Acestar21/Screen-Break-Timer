from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
)
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, Qt
import psutil
import time
import json
import os
import win32gui
import win32process
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Global data
class MonitorWorker(QThread):
    update_data = pyqtSignal(dict)
    update_label = pyqtSignal(str)

    def __init__(self, total_usage):
        super().__init__()
        self.total_usage = total_usage
        self.session_usage = {}
        self._running = True
        self.last_title = None
        self.last_switch_time = time.time()

    def get_active_app_name(self):
        hwnd = win32gui.GetForegroundWindow()
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid)
            return proc.name()
        except Exception:
            return "Unknown"

    def format_time(self, seconds):
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"

    def run(self):
        self.last_title = self.get_active_app_name()
        self.last_switch_time = time.time()

        while self._running:
            current_title = self.get_active_app_name()
            now = time.time()

            if current_title != self.last_title:
                time_spent = now - self.last_switch_time
                if self.last_title:
                    self.session_usage[self.last_title] = self.session_usage.get(self.last_title, 0) + time_spent
                self.last_title = current_title
                self.last_switch_time = now

            # Update label
            combined = self.total_usage.copy()
            for app, seconds in self.session_usage.items():
                combined[app] = combined.get(app, 0) + seconds

            text = "App Usage Summary:\n"
            for app, seconds in combined.items():
                text += f"{app}: {self.format_time(seconds)}\n"

            self.update_label.emit(text)
            self.update_data.emit(self.session_usage)
            time.sleep(1)

    def stop(self):
        self._running = False
        self.wait()

    def get_session_data(self):
        return self.session_usage


def load_today_usage():
    today = date.today().isoformat()
    file_path = f"Screen Care App/data/app_usage_{today}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def save_today_usage(total_usage, session_usage):
    today = date.today().isoformat()
    file_path = f"Screen Care App/data/app_usage_{today}.json"
    if not os.path.exists("data"):
        os.makedirs("data")

    combined = total_usage.copy()
    for app, seconds in session_usage.items():
        combined[app] = combined.get(app, 0) + seconds

    with open(file_path, "w") as f:
        json.dump(combined, f)
    print("Saved to", file_path)

class ScreenMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Monitor")
        self.setGeometry(200, 200, 800, 600)

        self.total_usage = load_today_usage()

        layout = QVBoxLayout()

        self.label = QLabel("App Usage Summary:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.label)

        self.canvas_frame = QFrame()
        self.canvas_layout = QVBoxLayout(self.canvas_frame)
        layout.addWidget(self.canvas_frame)

        button_layout = QHBoxLayout()
        self.show_graph_button = QPushButton("Show Graph")
        self.refresh_graph_button = QPushButton("Refresh Graph")
        self.close_button = QPushButton("Close")
        button_layout.addWidget(self.show_graph_button)
        button_layout.addWidget(self.refresh_graph_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.worker = MonitorWorker(self.total_usage)
        # self.worker.update_data.connect(self.draw_graph)
        self.worker.update_label.connect(self.label.setText)
        self.worker.start()

        self.show_graph_button.clicked.connect(lambda: self.draw_graph(self.worker.get_session_data()))
        self.refresh_graph_button.clicked.connect(lambda: self.draw_graph(self.worker.get_session_data()))
        self.close_button.clicked.connect(self.close_app)

    def draw_graph(self, session_data):
        # Combine total_usage and session_usage
        combined_data = self.total_usage.copy()
        for app, seconds in session_data.items():
            combined_data[app] = combined_data.get(app, 0) + seconds

    # Clear previous canvas
        for i in reversed(range(self.canvas_layout.count())):
            widget = self.canvas_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    # Prepare data
        apps = list(combined_data.keys())
        times = [combined_data[app] / 60 for app in apps]

    # Plot
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(apps, times, color='skyblue')
        ax.set_xlabel("Apps")
        ax.set_ylabel("Time (minutes)")
        ax.set_title("App Usage Graph")
        ax.set_xticklabels(apps, rotation=45, ha='right')
        fig.tight_layout()

    # Show on canvas
        canvas = FigureCanvas(fig)
        self.canvas_layout.addWidget(canvas)
        canvas.draw()


    def close_app(self):
        self.worker.stop()
        save_today_usage(self.total_usage, self.worker.get_session_data())
        self.close()


# To be used like:
# if __name__ == '__main__':
#     import sys
#     from PyQt6.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     window = ScreenMonitor()
#     window.show()
#     sys.exit(app.exec())
