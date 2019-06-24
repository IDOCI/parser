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
def fnParse(fname, arRe_tables, outfile, i):
    input_file = open(fname, encoding='utf-8')
    raw_text_data = input_file.read()
    iosFlag=False
    nxFlag=False
    errFlag=False
    if "IOS" in raw_text_data(1):
        iosFlag=True
    elif "NX-OS" in raw_text_data(1):
        nxFlag=True
    else :
        errFlag=True
    input_file.close()
    if iosFlag==True:
       re_table=arRe_tables["""посмотреть какое"""]
    if nxFlag==True:
        re_table=arRe_tables["""посмотреть какое"""]
    if errFlag==True:
       print ('Такого шаблона нет!')
    fsm_results = re_table.ParseText(raw_text_data)

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

#Получаем список файлов в переменную arRe_tables
patterns = os.listdir(tempdir)

arRe_tables=[]
for str in patterns:
    f=open(tempdir+'/'+str)
    arRe_tables.append(f)
    f.close()
## Сохранение в Excel (доделать)
# новая книга формата Excel:
wbk = xlwt.Workbook('utf-8')
# добавляем лист:
sheet = wbk.add_sheet('sheet 1')
## Временный вывод
#создаем список файлов, которые будем читать
files=os.listdir(directory)

# Результат пока что запишем в файл csv:
outfile_name = open(directory+"/outfile.csv", "w+")
outfile = outfile_name
print(re_table.header)
for s in re_table.header:
    outfile.write("%s;" % s)
outfile.write("\n")

#открываем файлы поочередно
trns=str.maketrans('','','\t\n\v\f\r')
for i,str in enumerate(files):
    if str.endswith('log'):
        fnParse(directory+'/'+str, re_table, outfile, i)

outfile.close()
