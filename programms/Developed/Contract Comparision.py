import tkinter as tk  
from tkinter import messagebox, scrolledtext, filedialog  
import pyodbc  
import pandas as pd  

# دیکشنری برای کوئری‌ها و استور پراسیجر  
queries = {  
    'Sheet1': "SELECT * FROM table_name",  # کوئری نمونه  
    'comparision_ReportAndExportToCsv': "{CALL [dbo].[sp_comparision_ReportAndExportToCsv](?,?,?,?)}"  # استور پراسیجر  
}  

# تابع برای انتخاب فایل خروجی  
def select_output_file():  
    output_file = filedialog.asksaveasfilename(defaultextension=".xlsx",  
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],  
                                                 title="Select Output File Path and Name")  
    entry_output_file.delete(0, tk.END)  
    entry_output_file.insert(0, output_file)  

# تابع برای کپی کردن محتویات تکست باکس  
def copy_to_clipboard():  
    root.clipboard_clear()  # پاک کردن کلیپ بورد  
    text = text_box.get("1.0", tk.END)  # دریافت متن از تکست باکس  
    root.clipboard_append(text)  # اضافه کردن متن به کلیپ بورد  
    messagebox.showinfo("Clipboard", "Text copied to clipboard!")  # نمایش پیام  

# تابع برای اجرای کوئری  
def execute_query():  
    new_year = int(entry_new_year.get())  
    old_year = int(entry_old_year.get())  
    from_month = int(entry_from_month.get())  
    to_month = int(entry_to_month.get())  
    server_name = entry_server_name.get()  
    bank_name = entry_bank_name.get()  
    table_name = entry_table_name.get()  
    output_file = entry_output_file.get()  

    try:  
        text_box.insert(tk.END, "Connecting to database...\n")  
        root.update()  

        connection_string = f"DRIVER={{SQL Server}};SERVER={server_name};DATABASE={bank_name};UID={entry_username.get()};PWD={entry_password.get()}"  
        conn = pyodbc.connect(connection_string)  
        cursor = conn.cursor()  

        text_box.insert(tk.END, "Connection successful.\n")  
        root.update()  

        # تست یک کوئری ساده  
        cursor.execute("SELECT 1")  # تست با یک کوئری ساده  
        result = cursor.fetchone()  
        text_box.insert(tk.END, f"Test query result: {result}\n")  

        results = {}  # دیکشنری برای ذخیره نتایج پرسش‌ها  

        # اجرای کوئری‌های واقعی  
        for sheet_name, query in queries.items():  
            try:  
                if 'sp_' in sheet_name:  # اگر نام شیت شامل 'sp_' است، این یک استور پراسیجر است  
                    # پارامترهای درست را برای استور پراسیجر ارسال کنید  
                    cursor.execute(query, from_month, to_month, new_year, old_year)  
                else:  
                    query = query.replace("table_name", table_name)  
                    cursor.execute(query)  
                results[sheet_name] = cursor.fetchall()  # نتایج را ذخیره کنید  
                text_box.insert(tk.END, f"Query '{sheet_name}' executed successfully.\n")  
            except Exception as e:  
                text_box.insert(tk.END, f"Error executing query '{sheet_name}': {str(e)}\n")  
                continue  

        # ذخیره نتایج به Excel  
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:  
            for sheet_name, result_set in results.items():  
                df = pd.DataFrame(result_set)  # تبدیل نتایج به DataFrame  
                short_sheet_name = sheet_name[:31]  # نام شیت باید حداکثر 31 کاراکتر باشد  
                df.to_excel(writer, sheet_name=short_sheet_name, index=False)  

                # تنظیمات شیت  
                worksheet = writer.sheets[short_sheet_name]  
                worksheet.sheet_view.rightToLeft = True  # تنظیم شیت به راست به چپ  
                worksheet.auto_filter.ref = worksheet.dimensions  # افزودن فیلتر به ستون‌ها  

        text_box.insert(tk.END, "Output saved successfully!\n")  

    except Exception as e:  
        text_box.insert(tk.END, f"Error: {str(e)}\n", fg='red')  
    finally:  
        cursor.close()  
        conn.close()  

def toggle_credentials():  
    is_windows_auth = var_auth_method.get() == "windows"  
    entry_username.config(state=tk.NORMAL if not is_windows_auth else tk.DISABLED)  
    entry_password.config(state=tk.NORMAL if not is_windows_auth else tk.DISABLED)  

# ایجاد پنجره اصلی  
root = tk.Tk()  
root.title("User Information Form")  

# فریم برای ورودی‌های سال و ماه  
frame_year_months = tk.Frame(root)  
frame_year_months.pack(pady=10, padx=10)  

# برچسب سال و ماه  
label_year_months = tk.Label(frame_year_months, text="Enter Year and Month:")  
label_year_months.grid(row=0, columnspan=8)  

label_new_year = tk.Label(frame_year_months, text="New Year:")  
label_new_year.grid(row=1, column=0, padx=5, pady=5)  

entry_new_year = tk.Entry(frame_year_months)  
entry_new_year.grid(row=1, column=1, padx=5, pady=5)  
entry_new_year.insert(0, "1403")  # مقدار پیش فرض  

label_old_year = tk.Label(frame_year_months, text="Old Year:")  
label_old_year.grid(row=1, column=2, padx=5, pady=5)  

entry_old_year = tk.Entry(frame_year_months)  
entry_old_year.grid(row=1, column=3, padx=5, pady=5)  
entry_old_year.insert(0, "1402")  # مقدار پیش فرض  

label_from_month = tk.Label(frame_year_months, text="From Month:")  
label_from_month.grid(row=1, column=4, padx=5, pady=5)  

entry_from_month = tk.Entry(frame_year_months)  
entry_from_month.grid(row=1, column=5, padx=5, pady=5)  
entry_from_month.insert(0, "2")  # مقدار پیش فرض  

label_to_month = tk.Label(frame_year_months, text="To Month:")  
label_to_month.grid(row=1, column=6, padx=5, pady=5)  

entry_to_month = tk.Entry(frame_year_months)  
entry_to_month.grid(row=1, column=7, padx=5, pady=5)  
entry_to_month.insert(0, "2")  # مقدار پیش فرض  

# فریم برای ورودی‌های نام سرور، بانک و جدول  
frame_server_bank_table = tk.Frame(root)  
frame_server_bank_table.pack(pady=10, padx=10)  

# برچسب برای سرور، بانک و جدول  
label_server_bank_table = tk.Label(frame_server_bank_table, text="Enter Server, Database, and Table Name:")  
label_server_bank_table.grid(row=0, columnspan=6)  

label_server_name = tk.Label(frame_server_bank_table, text="Server Name:")  
label_server_name.grid(row=1, column=0, padx=5, pady=5)  

entry_server_name = tk.Entry(frame_server_bank_table)  
entry_server_name.grid(row=1, column=1, padx=5, pady=5)  
entry_server_name.insert(0, "10.210.18.36\\mysql")  # مقدار پیش فرض  

label_bank_name = tk.Label(frame_server_bank_table, text="Bank Name:")  
label_bank_name.grid(row=1, column=2, padx=5, pady=5)  

entry_bank_name = tk.Entry(frame_server_bank_table)  
entry_bank_name.grid(row=1, column=3, padx=5, pady=5)  
entry_bank_name.insert(0, "top-sanj")  # مقدار پیش فرض  

label_table_name = tk.Label(frame_server_bank_table, text="Table Name:")  
label_table_name.grid(row=1, column=4, padx=5, pady=5)  

entry_table_name = tk.Entry(frame_server_bank_table)  
entry_table_name.grid(row=1, column=5, padx=5, pady=5)  
entry_table_name.insert(0, "contracts")  # مقدار پیش فرض  

# فریم برای انتخاب نوع احراز هویت  
frame_authentication = tk.Frame(root)  
frame_authentication.pack(pady=10)  

label_auth_method = tk.Label(frame_authentication, text="Authentication Method:")  
label_auth_method.pack(side=tk.LEFT, padx=5)  

var_auth_method = tk.StringVar(value="windows")  # مقداردهی اولیه  
radio_windows = tk.Radiobutton(frame_authentication, text="Windows", variable=var_auth_method, value="windows", command=toggle_credentials)  
radio_windows.pack(side=tk.LEFT)  

radio_sql = tk.Radiobutton(frame_authentication, text="SQL Server", variable=var_auth_method, value="sql", command=toggle_credentials)  
radio_sql.pack(side=tk.LEFT)  

# فریم برای نام کاربری و رمز عبور  
frame_credentials = tk.Frame(root)  
frame_credentials.pack(pady=10)  

label_username = tk.Label(frame_credentials, text="Username:")  
label_username.pack(side=tk.LEFT, padx=5)  

entry_username = tk.Entry(frame_credentials)  
entry_username.pack(side=tk.LEFT, padx=5)  

label_password = tk.Label(frame_credentials, text="Password:")  
label_password.pack(side=tk.LEFT, padx=5)  

entry_password = tk.Entry(frame_credentials, show="*")  
entry_password.pack(side=tk.LEFT)  

# فریم برای خروجی فایل  
frame_output_file = tk.Frame(root)  
frame_output_file.pack(pady=10)  

label_output_file = tk.Label(frame_output_file, text="Output File Path and Name:")  
label_output_file.pack(side=tk.LEFT, padx=5)  

entry_output_file = tk.Entry(frame_output_file, width=40)  
entry_output_file.pack(side=tk.LEFT, padx=5)  

output_button = tk.Button(frame_output_file, text="Browse", command=select_output_file)  
output_button.pack(side=tk.LEFT)  

# تکست باکس با ابعاد بزرگتر  
text_box = scrolledtext.ScrolledText(root, width=70, height=15)  
text_box.pack(pady=10)  

# دکمه اجرای کوئری  
execute_button = tk.Button(root, text="Execute Query", command=execute_query)  
execute_button.pack(pady=10)  

# دکمه کپی کردن محتویات تکست باکس  
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)  
copy_button.pack(pady=10)  

# تنظیمات پنجره  
toggle_credentials()  # برای تنظیم فیلدهای نام کاربری و رمز عبور در ابتدا  
root.mainloop()