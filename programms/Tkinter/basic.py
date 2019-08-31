from tkinter import *
from tkinter import ttk

root=Tk()
mainframe = ttk.Frame(root, padding="10 10 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


variable1=StringVar() # Value saved here

def search():
  print(variable1.get())
  return ''

ttk.Entry(mainframe, width=7, textvariable=variable1).grid(column=2, row=1)

ttk.Label(mainframe, text="label").grid(column=1, row=1)

ttk.Button(mainframe, text="Search", command=search).grid(column=2, row=13)

root.mainloop()
