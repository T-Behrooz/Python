import tkinter
from tkinter import *
top =Tk()
Label(top,text="Name :").grid(row=0,column=0)
e=Entry(top)
e.grid(row =0,column = 1)
b= Button(top,text = 'Press')
b.grid(row =1,column =2)
var = e.get()
e.bind('<Button-1>',print('str(var))'))
e.mainloop()
top.mainloop()
