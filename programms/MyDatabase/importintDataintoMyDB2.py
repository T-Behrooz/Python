ph = str(input("Enter The Path :"))
print(ph)
import os
x = os.listdir(ph)
print(x)
import pyodbc
con=pyodbc.connect("DRIVER={SQL Server};SERVER=localhost;DATABASE=sanj;UID=sa;PWD=110")
do=con.cursor()
for i in x:
    print(i)
    for j in range(1,13):
        sqlcommand= 'execute [sanj].[dbo].sp_importDatafrom_Excel \'contracts\',\''+ph+'\\'+str(i)+'\''+ ',' +'\''+ str(j)+'\''
        print(sqlcommand)
        do.execute(sqlcommand)
        do.commit()

sql="CREATE DATABASE test_new3;" #I added this for test
do.execute(sql)
con.close()