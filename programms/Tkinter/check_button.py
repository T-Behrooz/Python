from tkinter import *
from tkinter import ttk
root = Tk()
l = Label(root)
# def python():
#     l.config(text= 'python',fg ='red')
# def java():
#     l.config(text='java',fg = 'blue')
# cb1=ttk.Checkbutton(root,text= 'Python', state ='active',command = python)
# cb1.pack()
# cb2=Checkbutton(root,text= 'Java',command = java)
# cb2.pack()
P = StringVar()
J = StringVar()
P.set('This is set!')
cb3 = Checkbutton(root,text= 'String3 Test', variable = P ,onvalue =l.config(text= 'select TEst3',fg ='red'),offvalue =l.config(text= 'D select Test3',fg ='blue') )
cb3.pack()
# cb4 = Checkbutton(root,text= 'String4 Test', variable = J ,onvalue ="Selected !",offvalue ="Deslected!" )
# cb4.pack()
l.pack()
P.get()

root.mainloop()