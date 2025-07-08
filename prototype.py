import time
from tkinter import *
def show_pop_up():
    root = Tk()
    root.geometry('600x480+300+100')
    l = Label(root , text = 'Break Time' , font=("Times New Roman" , 48))
    l.pack(expand=True)
    root.after(2000, root.destroy)
    root.mainloop()


while True:
    print("Work time... (5 sec)")
    time.sleep(5)
    print("LOOK AWAY! (2 seconds)")
    show_pop_up()
    

