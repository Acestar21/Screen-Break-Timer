import threading
from tkinter import *
from screen_monitor import launch_monitor  

from screen_break_timer import start_break_timer , stop_timer
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
    btn_1.pack(pady=10)
    btn_2.pack(pady=10)
    btn_3.pack(pady=10)
    btn_4.pack(pady=10)
    btn_stop.pack(padx=10)
    root.mainloop()

menu()