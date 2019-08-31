import tkinter
 
window = tkinter.Tk()
window.geometry('200x200')
 
def showlocation(event):
     print(event.x, event.y)
 
window.bind('<B1-Motion>', showlocation)
 
window.mainloop()

