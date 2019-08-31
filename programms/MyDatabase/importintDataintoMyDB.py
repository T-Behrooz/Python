ph = str(input("Enter The Path ->"))
print(ph)
import os
x = os.listdir(ph)
print("number of files to be imported : ",len(x))
import pyodbc
con=pyodbc.connect("DRIVER={SQL Server};SERVER=localhost;DATABASE=sanj;UID=sa;PWD=110",autocommit=True)
do=con.cursor()
for i in x:
    print(i)
    for j in range(1,13):
        sheet=str(j)
        path= ph+'\\'+str(i)
        table = 'contracts'
        params=(table,path,sheet)
        try :
            do.execute("execute dbo.sp_importDatafrom_Excel ?,?,?" , params)
            do.commit()
            print( path +"("+sheet+")"+" Inserted")
        except NameError :
            print(NameError)

sql="CREATE DATABASE test_new3;"
do.execute(sql)
con.close()