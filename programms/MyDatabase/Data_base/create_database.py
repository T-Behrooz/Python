import pyodbc

db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;UID=sa; PWD=14;',autocommit=True)
#cursors=db.cursor()
sql="CREATE DATABASE test_new1;"
db.execute(sql)
#cursors.commit()

print(db.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES))

db.close()