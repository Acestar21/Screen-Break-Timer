from tkinter import *
import threading
import time
from datetime import datetime
import win32gui


app_usage = {}
last_title = None
last_switch_time = time.time()

def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd)
    return window_title

print("Current Active Window:", get_active_window_title())
try:
    while True:
        current_title = get_active_window_title()
        now = time.time()

        if current_title != last_title:
            if last_title:
                time_spent = now - last_switch_time
                app_usage[last_title] = app_usage.get(last_title, 0) + time_spent

            last_title = current_title
            last_switch_time = now

        # Show usage summary every few seconds (optional)
        if int(now) % 10 == 0:
            print("\nApp Usage Summary:")
            for app, seconds in app_usage.items():
                hrs = int(seconds // 3600)
                mins = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                print(f"{app}: {hrs:02d}:{mins:02d}:{secs:02d}")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nTracking stopped.")
    









# def screen_monitor():
#     root = Tk()
#     root.mainloop()

# screen_monitor()