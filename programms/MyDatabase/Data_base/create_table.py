import pyodbc
#host = "tizchang-pc"
#database = "test"
#username = "sa"
#password = "14"
#cs = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (host, username, password, database)
# 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=TIZCHANG-PC;database =test;UID=sa;PWD=14'
db=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=test;UID=sa;PWD=14')
cursors=db.cursor()
sql = """CREATE TABLE Persons1 (
    PersonID DECIMAL ,
    LastName nvarchar(255),
    FirstName nvarchar(255),
    Address nvarchar(255),
    City nvarchar(255)
);"""
try :

    cursors.execute(sql)
    cursors.commit()
except:
    print("ERROR")
db.close()
