from tkinter import *
from main import start_break_timer
def menu():
    root = Tk()
    root.title("menu")
    root.geometry("600x480")
    Label(root, text="Screen Care Assistant", font=("Arial", 18)).pack(pady=20)

    btn_1 = Button(root, text= "Screen timer", command=start_break_timer)
    btn_2 = Button(root, text= "Pomodoro timer")
    btn_3 = Button(root, text= "Screen monitor")
    btn_4 = Button(root, text= "Sound")
    btn_1.pack(pady=10)
    btn_2.pack(pady=10)
    btn_3.pack(pady=10)
    btn_4.pack(pady=10)
    root.mainloop()

menu()