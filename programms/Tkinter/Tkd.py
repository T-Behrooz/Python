
def Getval(i,root):
    sval1 = StringVar()
    l1 = Label(root, text=': کد ملی ')
    l1.grid(row=i, column=i)
    l1.pack(side='right')
    t1 = Entry(root, textvariables=svar1)
    t1.pack(side='right')
    return sval1