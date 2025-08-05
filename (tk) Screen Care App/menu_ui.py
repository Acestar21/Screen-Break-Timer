import threading
from tkinter import *
from screen_monitor import launch_monitor  
import json
from datetime import datetime, timedelta, date 
import time
import os
from screen_break_timer import start_break_timer , stop_timer


def today_usage():
    today = date.today().isoformat()
    file_path = f"data/app_usage_{today}.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            usage_data = json.load(file)

        for app, seconds in usage_data.items():
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            print(f"{app}: {hrs:02d}:{mins:02d}:{secs:02d}")
    else:
        print("No usage data available for today.")

def menu():
    root = Tk()
    root.title("menu")
    root.geometry("600x480")
    Label(root, text="Screen Care Assistant", font=("Arial", 18)).pack(pady=20)
    def screen_timer():
        thread = threading.Thread(target=start_break_timer)
        thread.daemon = True
        thread.start()

    btn_1 = Button(root, text= "Screen timer", command=screen_timer)
    btn_2 = Button(root, text= "Pomodoro timer")
    btn_3 = Button(root, text="Screen Monitor", command=launch_monitor)
    btn_4 = Button(root, text= "Sound")
    btn_stop = Button(root , text= "stop" , command=stop_timer)
    btn_5 = Button(root, text="View today usage", command=today_usage)
    btn_1.pack(pady=10)
    btn_2.pack(pady=10)
    btn_3.pack(pady=10)
    btn_4.pack(pady=10)
    btn_stop.pack(padx=10)
    btn_5.pack(pady=10)
    root.mainloop()

menu()