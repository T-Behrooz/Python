import time  
import pyodbc  
import pandas as pd  
from openpyxl import Workbook  
from openpyxl.utils import get_column_letter  
import tkinter as tk  
from tkinter import filedialog, messagebox, Scrollbar, ttk  

def log_message(message):  
    log_box.config(state=tk.NORMAL)  
    log_box.insert(tk.END, message + '\n')  
    log_box.see(tk.END)  
    log_box.config(state=tk.DISABLED)  

def execute_and_write_sql(sql_query, excel_sheet_name, success_message):  
    try:  
        df = pd.read_sql(sql_query, conn)  
        if not df.empty:  
            df.fillna(0, inplace=True)  
            df = df.applymap(lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x)  
            df.to_excel(writer, sheet_name=excel_sheet_name, index=False)  

            worksheet = writer.sheets[excel_sheet_name]  
            worksheet.auto_filter.ref = worksheet.dimensions  
            worksheet.sheet_view.rightToLeft = True  

            for column in range(1, len(df.columns) + 1):  
                column_letter = get_column_letter(column)  
                max_length = max(df[df.columns[column - 1]].astype(str).map(len).max(), len(column_letter) + 2)  
                worksheet.column_dimensions[column_letter].width = max_length  
            log_message(success_message)  
        else:  
            log_message(f"No data retrieved for sheet: {excel_sheet_name}")  
    except Exception as e:  
        log_message(f"An error occurred while processing {excel_sheet_name}: {e}")  

def connect_and_execute():  
    global conn, writer  

    server = server_entry.get()  
    database = database_entry.get()  
    table_name = table_entry.get()  
    output_file = f"{output_dir}/{output_file_entry.get()}.xlsx"  

    if win_auth_var.get():  
        username = ''  
        password = ''  
    else:  
        username = username_entry.get()  
        password = password_entry.get()  

    try:  
        if win_auth_var.get():  
            conn_str = f'DRIVER={driver_name};SERVER={server};DATABASE={database};Trusted_Connection=yes;Connection Timeout=30'  
        else:  
            conn_str = f'DRIVER={driver_name};SERVER={server};DATABASE={database};UID={username};PWD={password};Connection Timeout=30'  
        
        conn = pyodbc.connect(conn_str)  
        log_message("Connection established successfully.")  

        writer = pd.ExcelWriter(output_file, engine='openpyxl')  

        # تنظیم نوار پیشرفت  
        progress_bar['maximum'] = len(queries)  
        progress_bar['value'] = 0  

        for excel_sheet_name, sql_query in queries.items():  
            execute_and_write_sql(sql_query.format(table_name), excel_sheet_name, f"Data for {excel_sheet_name} written to Excel sheet successfully.")  
            progress_bar['value'] += 1  # به‌روزرسانی نوار پیشرفت  
            root.update_idletasks()  # به‌روزرسانی رابط کاربری  

        writer.close()  
        log_message("All data written to Excel successfully.")  

    except Exception as e:  
        log_message(f"Failed to connect to the database: {e}")  
    finally:  
        if 'conn' in locals():  
            conn.close()  

def browse_output_file_name():  
    output_file = filedialog.asksaveasfilename(defaultextension=".xlsx",  
                                                  filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],  
                                                  title="Select Output File Name")  
    if output_file:  
        output_file_entry.delete(0, tk.END)  
        output_file_entry.insert(0, output_file.split('/')[-1].split('.')[0])  # فقط نام فایل بدون مسیر و پسوند  
        global output_dir  # Make sure to use the global output_dir  
        output_dir = '/'.join(output_file.split('/')[:-1])  # Set the output directory to the selected path  

def toggle_username_password(show):  
    if show:  
        username_entry.config(state=tk.NORMAL)  
        password_entry.config(state=tk.NORMAL)  
    else:  
        username_entry.config(state=tk.DISABLED)  
        password_entry.config(state=tk.DISABLED)  

# دیکشنری کوئری‌ها  
queries = {  
    'Top10_Traffic_ASC': '''  
        select * from  
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service],[office] order by [diff-t] asc) as t_down from [{}]  
        ) ranks  
        where t_down <= 10  
    ''',  

    'Top10_Traffic_DESC': '''  
        select * from  
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service],[office] order by [diff-t] desc) as t_up from [{}]  
        ) ranks  
        where t_up <= 10  
    ''',  

    'Top10_Income_ASC': '''  
        select * from  
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service],[office] order by [diff-i] asc) as i_down from [{}]  
        ) ranks  
        where i_down <= 10  
    ''',  

    'Top10_Income_DESC': '''  
        select * from  
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service],[office] order by [diff-i] desc) as i_up from [{}]  
        ) ranks  
        where i_up <= 10  
    ''',  

    'total Top10_Traffic_DESC': '''  
        select * from   
        (  
            select top (10) ROW_NUMBER() OVER(ORDER BY [diff-t] DESC) AS tUP, * from [{}]  
            ORDER BY [diff-t] DESC  
        ) as t_Up ORDER BY [office]   
    ''',       
    
    'total Top10_Traffic_ASC': '''  
        select * from   
        (  
            select top (10) ROW_NUMBER() OVER(ORDER BY [diff-t] ASC) AS tdown, * from [{}]  
            ORDER BY [diff-t] DESC  
        ) as t_down ORDER BY [office]   
    ''',   
    
    'total Top10_Income_DESC': '''  
        SELECT * FROM   
        (  
            select top (10) ROW_NUMBER() OVER(ORDER BY [diff-i] DESC) AS iUP, * from [{}]   
            ORDER BY [diff-i] DESC  
        ) as i_Up ORDER BY [office]  
    ''',  
    
    'total Top10_Income_ASC': '''  
        SELECT * FROM   
        (  
            select top (10) ROW_NUMBER() OVER(ORDER BY [diff-i] ASC) AS iUP, * from [{}]   
            ORDER BY [diff-i] DESC  
        ) as i_Up ORDER BY [office]  
    ''',  
    
    'Services Top10_Traffic_ASC': '''  
        select * from   
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service] order by [diff-t] asc) as t_down from [{}]  
        ) ranks  
        where t_down <= 10  
    ''',  
    
    'Services Top10_Traffic_DESC': '''  
        select * from   
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service] order by [diff-t] desc) as t_up from [{}]  
        ) ranks  
        where t_up <= 10   
    ''',  
    
    'Services Top10_Income_ASC': '''  
        select * from   
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service] order by [diff-i] asc) as i_down from [{}]  
        ) ranks  
        where i_down <= 10  
    ''',  
    
    'Services Top10_Income_DESC': '''  
        select * from   
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service] order by [diff-i] desc) as i_down from [{}]  
        ) ranks  
        where i_down <= 10  
    ''',  
    
    'ServicesTop10City_Traffic_ASC': '''  
        select * from   
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service],[office] order by [diff-t] asc) as t_down from [{}]  
        ) ranks  
        where t_down <= 10  
    ''',  
     
    'ServicesTop10City_Traffic_DESC': '''  
        select * from   
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service],[office] order by [diff-t] desc) as t_up from [{}]  
        ) ranks  
        where t_up <= 10   
    ''',  
    
    'ServicesTop10City_Income_ASC': '''  
        select * from   
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service],[office] order by [diff-i] asc) as i_down from [{}]  
        ) ranks  
        where i_down <= 10  
    ''',  
    
    'ServicesTop10City_Income_DESC': '''  
        select * from   
        (  
            select [office],[name],[service],[old-t],[old-i],[new-t],[new-i],[old-phi],[new-phi],[diff-t],[diff-i],  
            ROW_NUMBER() over(partition by [service],[office] order by [diff-i] desc) as i_up from [{}]  
        ) ranks  
        where i_up<= 10 
    ''',
}

# رابط گرافیکی   
root = tk.Tk()  
root.title("SQL to Excel Exporter v.1")  
root.geometry("700x600")  # تنظیم ابعاد اولیه فرم  

# ورودی آدرس سرور، نام بانک، و نام جدول  
tk.Label(root, text="Server Address:").grid(row=0, column=0, padx=5, pady=5, sticky='w')  
server_entry = tk.Entry(root)  
server_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')  
server_entry.insert(0, "10.210.18.36\\mysql")
tk.Label(root, text="Database Name:").grid(row=1, column=0, padx=5, pady=5, sticky='w')  
database_entry = tk.Entry(root)  
database_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')  
database_entry.insert(0, "top-sanj")
tk.Label(root, text="Table Name:").grid(row=2, column=0, padx=5, pady=5, sticky='w')  
table_entry = tk.Entry(root)  
table_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')  
table_entry.insert(0, "mah")
tk.Label(root, text="Output File Name:").grid(row=3, column=0, padx=5, pady=5, sticky='w')  
output_file_entry = tk.Entry(root)  
output_file_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')  
tk.Button(root, text="Browse", command=browse_output_file_name).grid(row=3, column=2, padx=5, pady=5)  

# نوع احراز هویت  
win_auth_var = tk.BooleanVar(value=True)  
tk.Radiobutton(root, text="Windows Authentication", variable=win_auth_var, value=True, command=lambda: toggle_username_password(False)).grid(row=4, column=0, padx=5, pady=5, sticky='w')  
tk.Radiobutton(root, text="SQL Server Authentication", variable=win_auth_var, value=False, command=lambda: toggle_username_password(True)).grid(row=4, column=1, padx=5, pady=5, sticky='w')  

tk.Label(root, text="Username:").grid(row=5, column=0, padx=5, pady=5, sticky='w')  
username_entry = tk.Entry(root)  
username_entry.grid(row=5, column=1, padx=5, pady=5, sticky='ew')  

tk.Label(root, text="Password:").grid(row=6, column=0, padx=5, pady=5, sticky='w')  
password_entry = tk.Entry(root, show="*")  
password_entry.grid(row=6, column=1, padx=5, pady=5, sticky='ew')  

# نوار پیشرفت  
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")  
progress_bar.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='ew')  

# دکمه اجرای برنامه  
execute_button = tk.Button(root, text="Execute Queries", command=connect_and_execute)  
execute_button.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky='ew')  

# کنترل نمایش پیام‌ها  
tk.Label(root, text="Execution Log:").grid(row=9, column=0, padx=5, pady=5, sticky='w')  
log_box = tk.Text(root, width=60, height=15)  
log_box.grid(row=10, column=0, columnspan=3, padx=5, pady=5, sticky='ew')  
log_box.config(state=tk.NORMAL)  # تنظیم حالت برای نوشتن در کنترل  
log_box.config(state=tk.DISABLED)  # غیرفعال کردن ویرایش  

# نمایش نوار اسکرول  
scrollbar = Scrollbar(root, command=log_box.yview)  
scrollbar.grid(row=10, column=3, sticky='ns')  
log_box.config(yscrollcommand=scrollbar.set)  

# تنظیم اولیه بین نام کاربری و رمز  
toggle_username_password(not win_auth_var.get())  # تنظیم اولیه  

# راه‌اندازی درایور  
driver_name = ''  
output_dir = ''  # هیچ چیز به طور پیش‌فرض انتخاب نشد  
driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]  
if driver_names:  
    driver_name = driver_names[0]  

# تنظیمات برای فیکس کردن اندازه فرم  
root.grid_rowconfigure(0, weight=1)  
root.grid_rowconfigure(1, weight=1)  
root.grid_rowconfigure(2, weight=1)  
root.grid_rowconfigure(3, weight=1)  
root.grid_rowconfigure(4, weight=1)  
root.grid_rowconfigure(5, weight=1)  
root.grid_rowconfigure(6, weight=1)  
root.grid_rowconfigure(7, weight=1)  
root.grid_rowconfigure(8, weight=1)  
root.grid_rowconfigure(9, weight=1)  
root.grid_rowconfigure(10, weight=1)  
root.grid_columnconfigure(0, weight=1)  
root.grid_columnconfigure(1, weight=1)  
root.grid_columnconfigure(2, weight=1)  

root.mainloop()