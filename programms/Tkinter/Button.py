from tkinter import *
from tkinter import ttk
root = Tk()
b1 = ttk.Button(root,text="My First ttk")
#b1.config(bd=5)
b1.pack()
b2 = Button(root,text="My First Button!")
b2.config(bd=5)
b2.config(activebackground = 'yellow')
b2.config(activeforeground = 'red')
b2.config(highlightcolor = '#fff')
b2.pack()
root.mainloop()