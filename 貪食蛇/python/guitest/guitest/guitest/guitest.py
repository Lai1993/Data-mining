#import tkinter as tk
#from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import time
win=Tk()
win.title("ttk GUI")
label=Label(win, text="Hello World!")
count=0
def clickOK():
    global count
    count=count + 1
    label.config(text="Click OK " + str(count) + " times")
label.pack()
button=Button(win, text="OK", command=clickOK)
button.pack()
def clock():
    t=time.strftime('%I:%M:%S',time.localtime())
    if t!='':
        label2.config(text=t,font='times 25')
    win.after(100,clock)
label2=Label(win,justify='center')
label2.pack()
clock()
win.mainloop()