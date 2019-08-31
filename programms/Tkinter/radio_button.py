from tkinter import *

class Myapp:


    def __init__(self,root):

        self.var = StringVar()
        self.rd1 = Radiobutton(root,text = 'I need help!',variable = self.var , value = 'Yes', command=self.selecty)
        self.rd1.grid( row =0 , column =1)
        self.rd2 = Radiobutton(root, text='I do not need help!', variable = self.var, value='No', command=self.selecty)
        self.rd2.grid( row =1 , column =2)
        self.rd1.config(cursor='star')
        self.rd2.config(cursor='mouse')

    def selecty(self):
        print(self.var.get())


def main():
	root = Tk()
	app = Myapp(root)
	root.mainloop()
    # root.var.get()
    # print(var.get())

if __name__ == "__main__":
	main()