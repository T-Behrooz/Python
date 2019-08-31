from tkinter import *
root = Tk()

def Mycoman ():
    print('You pressed command Button!')

x= Button (root,text = 'Change', command = Mycoman)
x.grid(row =10,column = 10)
x.pack()
x.mainloop()
