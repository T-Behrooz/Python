from tkinter import *
import Tkd
root = Tk()
root.title('Data Entry')
#-------------------------------------------
svar1=StringVar()
l1 = Label(root, text=': کد ملی ')
#l1.grid(row=1, column=1)
l1.pack(side='right')
t1= Entry(root,textvariable=svar1)
t1.pack(side='right')
#----------------------------------------------
svar3= StringVar()
l3 = Label(root, text=': نام خانوادگی ')
#l3.grid(row = 3,column = 1)
l3.pack(side='right')
t3= Entry(root,textvariable=svar3)
t3.pack(side='right')
#-----------------------------------------------
svar5= StringVar()
l5 =Label(root, text=': نام ')
#l5.grid(row=5, column=5)
l5.pack(side='right')
t5=Entry(root,textvariable=svar5)
t5.pack(side='right')
#-----------------------------------------------
svar7= StringVar()
l7 =Label(root, text=': آدرس ')
#l7.grid(row=7, column=7)
l7.pack(side='right')
t7=Entry(root,textvariable=svar7)
t7.pack(side='right')
#------------------------------------------------
svar9= StringVar()
l9 =Label(root, text=': شهر ')
#l9.grid(row=9, column=9)
l9.pack(side='right')
t9=Entry(root,textvariable=svar9)
t9.pack(side='right')
#----------------------------------------------------
def insert_line():
    import pyodbc
    con=pyodbc.connect("DRIVER={SQL Server};SERVER=localhost;DATABASE=test;UID=sa;PWD=14")
    do=con.cursor()
    #values=[svar1,svar3,svar5,svar7,svar9]
    sqlcommand="INSERT INTO Persons values({},{},{},{},{});"%(int(svar1.get()),str(svar3.get()),str(svar5.get()),str(svar7.get()),str(svar9.get()))
    do.execute(sqlcommand,values)
    do.commit()
# #-------------------------------------------------------
#def pp():
   # print(svar1.get(),svar11)
    # print(svar3, svar3.get(), type(svar3),type(svar3.get()))
    # print(svar5, svar5.get(), type(svar5),type(svar5.get()))
    # print(svar7, svar7.get(), type(svar7),type(svar7.get()))
    # print(svar9, svar9.get(), type(svar9),type(svar9.get()))
b = Button(root,text='Insert',command = insert_line)
b.pack()
root.mainloop()