import pyodbc
import pandas as pd

cnxn = pyodbc.connect(("DRIVER={SQL Server};SERVER=localhost;DATABASE=test;UID=sa;PWD=14"))
cursor = cnxn.cursor()
script = """
SELECT * FROM persons
"""
path="D:\\268\\behrooz.xlsx"


# columns = [desc[0] for desc in cursor.description]
# data = cursor.fetchall()
# df = pd.DataFrame(list(data), columns=columns)
#
# writer = pd.ExcelWriter(path)
# df.to_excel(writer, sheet_name='bar')
# writer.save()
cursor.execute(script)
rows = cursor.fetchall()

for x in rows :
   print(x.UID)