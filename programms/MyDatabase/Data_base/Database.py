import pyodbc
test='y'
dm = input("آیا می خواهید ورود اطلاعات انجام دهید ؟(y/n)")
if dm=='y':
    count=0
    con=pyodbc.connect("DRIVER={SQL Server};SERVER=localhost;DATABASE=test;UID=sa;PWD=14")
    do=con.cursor()
    while (test=='y'):
       personid=int(input("کد ملي :"))
       lastname=str(input("نام خانوادگي :"))
       firstname=str(input("نام :"))
       address =str(input("آدرس :"))
       city = str(input("شهر :"))
       values=[personid,lastname,firstname,address,city]
       sqlcommand="INSERT INTO Persons1 values(?,?,?,?,?);"
       do.execute(sqlcommand,values)
       do.commit()
       count+=1
       test=input("ادامه مي دهيد ؟(y/n)")
       do.close()
    print("%d سطر وارد شد" % count)
else :
    dm = input("آیا می خواهید ورود گزارش گیری انجام دهید ؟(y/n)")
    if dm =='y':
        con = pyodbc.connect("DRIVER={SQL Server};SERVER=localhost;DATABASE=test;UID=sa;PWD=14")
        do = con.cursor()
        row=do.execute("select * from persons1")
        for i in row :
            print (i)
        print("-----------------------------------------------------")
        row=do.execute("select * from persons1")
        for i in row :
            print("--------------------------------------------------------------------------")
            print ("کد ملي:|",i[0],"|نام خانوادگي:",i[1],"|نام :",i[2]," | آدرس :",i[3],"| شهر:",i[4])
            print("--------------------------------------------------------------------------")
    else :
       input("برای خروج از برنامه کلیدی را فشار دهید...")
