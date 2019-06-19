import textfsm
import os
import re
import xlwt
import tkinter as tk
from tkinter import filedialog
def fnParse(fname, re_table, outfile, i):
    input_file = open(fname, encoding='utf-8')
    raw_text_data = input_file.read()
    input_file.close()

    fsm_results = re_table.ParseText(raw_text_data)



    # ...now all row's which were parsed by TextFSM
    counter = 0
    for row in fsm_results:
        print(row)
        for s in row:
            outfile.write("%s;" % s)
        outfile.write("\n")
        counter += 1
    print("Write %d records" % counter)

directory=filedialog.askdirectory()#Выбор директории по диалоговому окну
# Читаем файл шаблона:
# Run the text through the FSM.
# The argument 'template' is a file handle and 'raw_text_data' is a
# string with the content from the show_inventory.txt file
template = open(directory+"/show_inventory_multiple.textfsm")
re_table = textfsm.TextFSM(template)

# новая книга формата Excel:
wbk = xlwt.Workbook('utf-8')
# добавляем лист:
sheet = wbk.add_sheet('sheet 1')

#создаем список файлов, которые будем читать

files=os.listdir(directory)

# Результат пока что запишем в файл csv:
outfile_name = open(directory+"/outfile.csv", "w+")
outfile = outfile_name

# Display result as CSV and write it to the output file
# First the column headers...
print(re_table.header)
for s in re_table.header:
    outfile.write("%s;" % s)
outfile.write("\n")

#открываем файлы поочередно
trns=str.maketrans('','','\t\n\v\f\r')
for i,str in enumerate(files):
    if str.endswith('log'):
        fnParse('c:/config/'+str, re_table, outfile, i)

outfile.close()
