import tkinter
from tkinter import *
 
window = tkinter.Tk()
window.geometry('200x200')
button = Button(window, text='Click Me!')
button.pack()
 
def showmessage(event):
     print("You clicked the button!")
 
button.bind('<Button>', showmessage)
 
window.mainloop()
button.mainloop()
