'''
Use this to take a HEX stream copied from wireshark and write to an excel file with 2 bytes per line
'''
import numpy as np
import xlsxwriter

with open("sine0_bin.txt", "r") as f:
    data = f.read()

print(data[0:40])

values = []
temp = ''
for idx, val in enumerate(data):
    temp += val
    if (idx+1) % 4 == 0:
        values.append(temp)
        temp = ''

print(values[0:10])
print(len(values))

with xlsxwriter.Workbook('sine0_bin.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(values):
        worksheet.write_row(row_num, 0, [data])
