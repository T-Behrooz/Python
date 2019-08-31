import tkinter as tk

# if you are still working under a Python 2 version,
# comment out the previous line and uncomment the following line
# import Tkinter as tk

root = tk.Tk()
root.title('اولین فرم من')
root.geometry('500x700')
w1 = tk.Label(root, text="Hello Tkinter!")
w1.pack()
#w2 = tk.Text(root,text=)
root.mainloop()
