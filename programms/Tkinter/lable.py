from tkinter import *

root = Tk()
l1 = Label(root, text="By using an appropriate combination of red,"
                      " green, and blue intensities, many colors can be displayed."
                      " Current typical display adapters use up to 24-bits of information for each pixel"
                      ": 8-bit per component multiplied by three components. With this system, 16,777,216 (2563 or 224) discrete "
                      "combinations of R, G and B values are allowed, providing millions of different (though not necessarily"
                      " distinguishable) hue, saturation, and lightness shades.")
l1.config(wraplen=300)
l1.config(justify = LEFT)
l1.config(bg='#303952')
l1.config(fg='#cf6a87')
path='c:\\1.png'
img =PhotoImage(file = path)
l1.config(image=img)
l1.config(compound = LEFT)
l1.config(bd=20)
l1.pack()
l1.config(height =400 )
l1.config(width =600 )
l1.config(padx=5)
l1.config(pady=10)
l2 = Label(root, text='Second lable')
l2.config(relief = 'sunken')
l2.config(padx=5)
l2.config(pady=10)
l2.config(height =50 )
l2.config(width =200 )
l2.pack()
root.mainloop()