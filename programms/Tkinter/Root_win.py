from tkinter import *
root = Tk(className = "MyApp")
def pp():
    Label(root,text = b.cget('bg')).pack()

b = Button(root,text="My First Button!",bg ='blue',fg='yellow',command = pp)
b.pack()
root.mainloop()