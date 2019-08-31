import openpyxl
wb = openpyxl.load_workbook('tradeName.xlsx')
type(wb)
wb.get_sheet_names()
