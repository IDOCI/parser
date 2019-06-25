import textfsm
import os
import re
import xlwt
import tkinter as tk
from tkinter import filedialog
from tkinter import Tk
## tkinter

#Закрытие системного окна tkinter
root = Tk()
root.withdraw()

## Функция
def fnParse(fname, arRe_tables, arOutFiles):
    input_file = open(fname, encoding='utf-8')
    raw_text_data = input_file.read()
    for i,tbl in enumerate(arRe_tables):
        outfile=arOutFiles[i]
        fsm_results = tbl.ParseText(raw_text_data)
        counter = 0
        for row in fsm_results:
            print(row)
            for s in row:
                outfile.write("%s;" % s)
            outfile.write("\n")
            counter += 1
        print("Write %d records" % counter)

## Диалоговое окно
#Выбор директории по диалоговому окну
directory=filedialog.askdirectory(title='Please select a directory')

## Читаем файлы шаблонов

#Каталог из которого будем брать шаблон
tempdir= (directory+'/templates')
patterns=''

#Получаем список таблиц преобразования в переменную arRe_tables
patterns = os.listdir(tempdir)
arRe_tables=[]
arOutf=[]
for i,str in enumerate( patterns):
    f=open(tempdir+'/'+str)
    tbl=textfsm.TextFSM(f)
    arRe_tables.append(tbl)
    ss=f"{directory}/outfile_{i}.csv"
    arOutf.append(open(ss, "w+"))

    f.close()
## Сохранение в Excel (доделать)
# новая книга формата Excel:
wbk = xlwt.Workbook('utf-8')
# добавляем лист:
sheet = wbk.add_sheet('sheet 1')
## Временный вывод

#создаем список файлов, которые будем читать
files=os.listdir(directory)
for fname in files:
    if fname.endswith('.log'):
        fnParse(directory+"/"+fname, arRe_tables, arOutf)

#
#
# print(arRe_tables[0])
# for i,tbl in enumerate(arRe_tables):
#     f=arOutf[i]
#     for s in tbl.header:
#         f.write("%s;" % s)
#     f.write("\n")
#
# #открываем файлы поочередно
# trns=str.maketrans('','','\t\n\v\f\r')
# for i,str in enumerate(files):
#     if str.endswith('log'):
#         for j,tbl in enumerate(arRe_tables):
#             fnParse(directory+'/'+str, tbl, arOutf(j), i)
#
# outfile.close()
for f in arOutf:
    f.close()