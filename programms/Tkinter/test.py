import tkinter
from tkinter import *
win =Tk()
win.geometry('200x100')
win.title('Multiple')
label = Label(win, text = 'Number:').pack()
in1 = Entry(win).pack()
str1='Result will be !'
button1=Button(win,text='Press to Multiple the Numers')
button1.pack()
def Multiple(event):
    str1= event.keysym
    label1 = Label(win, text = str1,fg = 'red',bg ='yellow').pack()
button1.bind('<Button-3>',Multiple)
win.mainloop()
button1.mainloop()


top =Tk()
Lable(top,text="we").grid(row=0,column=1)
e=Entry(top)
e.grid(row =0,column = 0)
top.mainloop()
