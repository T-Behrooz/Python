# -*- coding: utf-8 -*-  
"""  
Created on Sat Sep  7 10:15:35 2024  

@author: Tizchang  
"""  

import pyodbc   
import pandas as pd  

##############################################################################  
file_name = 'd:\\out_put.xlsx'  
driver_name = ''  
##############################################################################  

# Identify suitable SQL Server driver  
driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]  
if driver_names:  
    driver_name = driver_names[0]  

if driver_name:  
    SERVER = '10.210.18.36\\mysql'  # Changed backslash to double for escaping  
    DATABASE = 'top-sanj'  
    Trusted = 'yes'  
    conn_str = f'DRIVER={driver_name};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection={Trusted}'  
else:  
    print('(No suitable driver found. Cannot connect.')   
    exit(1)  # Exit the script if no driver is found  

# --------------------------- connection ------------------------------------  

try:  
    conn = pyodbc.connect(conn_str)  
    cursor = conn.cursor()  
    print("Connection established successfully.")  
except Exception as e:  
    print(f"Failed to connect to the database: {e}")  
    exit(1)  

# Use ExcelWriter to write to the same file  
with pd.ExcelWriter(file_name, engine='openpyxl') as writer:  
    try:  
        # Test with a simple query instead of the stored procedure  
        print("Executing simple query to test results.")  
        cursor.execute("SELECT TOP 10 * FROM mah")  # Change this to your table name  
        
        # Fetch the first result  
        current_result = cursor.fetchall()  

        # Check if there are any results  
        if not current_result:  
            print("No results returned from the simple query.")  
        else:  
            # Get the column names  
            columns = [column[0] for column in cursor.description]  
            print(f"Query returned {len(current_result)} rows and the following columns: {columns}")  

            # Print the fetched data for debugging  
            for row in current_result:  
                print(row)  # Each row will be a tuple, check how they appear  
            
            # Create a DataFrame  
            df = pd.DataFrame.from_records(current_result, columns=columns)  

            print(f"DataFrame created with shape: {df.shape}")  

            # Write DataFrame to a new sheet in the Excel file  
            df.to_excel(writer, sheet_name='Simple_Query_Result', index=False)  
            print("Data written to Excel file successfully.")  

    except Exception as e:  
        print(f"An error occurred: {e}")  

cursor.close()  
conn.close()   
print("Connection closed.")