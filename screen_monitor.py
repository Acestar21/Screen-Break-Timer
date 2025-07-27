from tkinter import *
import threading
import time
import psutil
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import win32gui
import win32process
import json, os
from datetime import date



total_usage = {}    # Holds data loaded from JSON (all previous runs)
session_usage = {}  # Holds only this session's new data

last_title = [None]
last_switch_time = [time.time()]

def load_today_usage():
    today = date.today().isoformat()
    file_path = f"data/app_usage_{today}.json"
    if os.path.exists(file_path):
        print("loading")
        with open(file_path, "r") as f:
            return json.load(f) 
             # returns the dictionary
    return {}  # no file → start fresh
    


def save_today_usage(session_usage):
    global total_usage
    today = date.today().isoformat()
    file_path = f"data/app_usage_{today}.json"
    if not os.path.exists("data"):
        os.makedirs("data")

    # Start with previous total_usage
    combined = total_usage.copy()
    # Add session_usage
    for app, seconds in session_usage.items():
        combined[app] = combined.get(app, 0) + seconds

    with open(file_path, "w") as f:
        json.dump(combined, f)

    print("saving...")

 
def get_active_app_name():
    hwnd = win32gui.GetForegroundWindow()
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        return proc.name()
    except Exception:
        return "Unknown"

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

def draw_bar_chart(frame, usage_data):
    for widget in frame.winfo_children():
        widget.destroy()
    apps = list(usage_data.keys())
    times = [usage_data[app] / 60 for app in apps]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(apps, times, color='skyblue')
    ax.set_xlabel("Time Spent (minutes)")
    ax.set_title("App Usage")
    ax.set_xticklabels(apps, rotation=45, ha='right')
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def update_text_display(label,session_usage):
    combined = total_usage.copy()
    for app, seconds in session_usage.items():
        combined[app] = combined.get(app, 0) + seconds

    text = "App Usage Summary:\n"
    for app, seconds in combined.items():
        text += f"{app}: {format_time(seconds)}\n"
    label.config(text=text)


def maybe_draw_chart(graph_frame):
    draw_bar_chart(graph_frame, session_usage)


def screen_monitor():
    global total_usage, session_usage
    root = Tk()
    root.title("Screen Monitor")
    root.geometry("800x640")

    text_label = Label(root, text="Tracking...", font=("Arial", 14), justify=LEFT)
    text_label.pack(pady=10)

    graph_frame = Frame(root)
    graph_frame.pack()
    
    canvas = [None]  # So we can modify it inside inner functions
    show_graph_button = Button(root, text="Show App Usage Graph")
    refresh_graph_button = Button(root, text="Refresh Graph")
    close_graph_button = Button(root, text="Close Graph")

    def draw_and_show_graph():
        for widget in graph_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(5, 3))
        apps = list(session_usage.keys())
        times = [session_usage[app] / 60 for app in apps]
        ax.bar(apps, times, color='skyblue')
        ax.set_xlabel("Time Spent (minutes)")
        ax.set_title("App Usage")
        ax.set_xticklabels(apps, rotation=45, ha='right')
        fig.tight_layout()
        canvas[0] = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas[0].draw()
        canvas[0].get_tk_widget().pack()

    def show_graph():
        show_graph_button.pack_forget()
        draw_and_show_graph()
        refresh_graph_button.pack()
        close_graph_button.pack()

    def refresh_graph():
        draw_and_show_graph()

    def close_graph():
        for widget in graph_frame.winfo_children():
            widget.destroy()
        refresh_graph_button.pack_forget()
        close_graph_button.pack_forget()
        show_graph_button.pack()

    # Bind commands
    show_graph_button.config(command=show_graph)
    refresh_graph_button.config(command=refresh_graph)
    close_graph_button.config(command=close_graph)

    # Initial pack
    show_graph_button.pack(pady=10)
    total_usage = load_today_usage()
    session_usage = {}  
    last_title[0] = get_active_app_name()
    last_switch_time[0] = time.time()
    first_run = [True] 
    def track_usage():
        global session_usage, last_title, last_switch_time
        current_title = get_active_app_name()
        now = time.time()

    # Skip adding time on very first loop
        if first_run[0]:
            last_title[0] = current_title
            last_switch_time[0] = now
            first_run[0] = False

        if current_title != last_title[0]:
            time_spent = now - last_switch_time[0]
            session_usage[last_title[0]] =session_usage.get(last_title[0], 0) + time_spent
            last_title[0] = current_title
            last_switch_time[0] = now

        update_text_display(text_label,session_usage)
        root.after(1000, track_usage)
  # repeat every second

    def on_close():
        global session_usage
        save_today_usage(session_usage)
        print("Closing app... and save")
        root.destroy()  # Close the window
        exit()          # Ensure the whole program exits

    root.protocol("WM_DELETE_WINDOW", on_close)
    

    track_usage()
    
    root.mainloop()

def launch_monitor():
    screen_monitor()    