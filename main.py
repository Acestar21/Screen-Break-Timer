import time
from tkinter import *
import threading
stop_event = threading.Event()
def show_pop_up():
    root = Tk()
    root.geometry('600x480+300+100')
    l = Label(root , text = 'Break Time' , font=("Times New Roman" , 48))
    l.pack(expand=True)
    root.after(2000 , root.destroy)
    root.mainloop()


def start_break_timer():
    while not stop_event.is_set():
        print("Work time... (5 seconds)")
        time.sleep(5)
        print("LOOK AWAY! (2 seconds)")
        show_pop_up()
    print("the loop is stopped")

def stop_timer():
    stop_event.set()
