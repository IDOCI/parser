import textfsm
import os
import re
import xlwt
import tkinter as tk
from tkinter import filedialog
from tkinter import Tk
from pyexcel.book import Book
from pyexcel.core import save_as, get_sheet
from pyexcel_xlsxw import save_data
#раскомментировать, если надо удалить папку results
#import shutil
## tkinter

#Закрытие системного окна tkinter
root = Tk()
root.withdraw()

## Функция
def fnParse(fname, arPatFnames, arOutFiles,log):
    log=''
    done=False
    input_file = open(fname, encoding='utf-8')
    input_file.readline()
    ss=input_file.readline()
    if 'Cisco IOS' in ss:
        word='IOS'
    elif 'Cisco Nexus' in ss:
        word='nxos'
    else:
        word=''
    input_file.close()
    for i,str in enumerate(arPatFnames):
        if (word=='') or (word.lower() in str.lower()):
            input_file = open(fname, encoding='utf-8')
            raw_text_data = input_file.read()
            input_file.close()
            outfile=arOutFiles[i]
            f=open(tempdir+'/'+str)
            tbl = textfsm.TextFSM(f)
            f.close()
            try:
                fsm_results = tbl.ParseText(raw_text_data)

                OK=True
            except:
                OK=False

            if OK:
                counter = 0
                for row in fsm_results:
                    for s in row:
                        done=True
                        outfile.write("%s;" % s)
                    outfile.write("\n")
                    counter += 1
    if done:
        log+="Parsed "+fname+'\n'
        print("\x1b[32mParsed "+fname+"\x1b[0m")

    else:
        log+="Not parsed "+fname+'\n'
        print("\x1b[31mNot parsed "+fname+"\x1b[0m")
    logfile.write(log)



## Диалоговое окно
#Выбор директории по диалоговому окну
directory=filedialog.askdirectory(title='Please select logs directory')

## Читаем файлы шаблонов

#Каталог из которого будем брать шаблон
tempdir= filedialog.askdirectory(title='Please select templates directory')
#tempdir= (directory+'/templates')
patterns=''

#Получаем список таблиц преобразования в переменную arRe_tables
patterns = os.listdir(tempdir)
arPatFnames=[]
arOutf=[]
for i,str in enumerate(patterns):
    arPatFnames.append(str)
    ss=f"{directory}/../results/result_{str.replace('.template','')}.csv"
    if not os.path.isdir(f"{directory}/../results"):
        os.makedirs(f"{directory}/../results")
    outfile=open(ss, "w+")
    arOutf.append(outfile)
    f=open(tempdir+'/'+str)
    tbl = textfsm.TextFSM(f)
    for s in tbl.header:
        outfile.write("%s;" % s)
    outfile.write("\n")
    f.close()
## Сохранение в Excel (доделать)
# новая книга формата Excel:
wbk = xlwt.Workbook('utf-8')
# добавляем лист:
sheet = wbk.add_sheet('sheet 1')
## Временный вывод

#создаем список файлов, которые будем читать
files=os.listdir(directory)
logss=f"{directory}/../logfile.log"
logfile=open(logss, "w+")
log=''
for fname in files:
    if fname.endswith('.log'):
        fnParse(f"{directory}/{fname}", arPatFnames, arOutf, log)
logfile.close()

for f in arOutf:
    f.close()
def merge_csv_to_a_book(filelist, outfilename):

    merged = Book()
    for file_name in filelist:
        sheet = get_sheet(file_name=file_name,delimiter=';')
        _, tail = os.path.split(file_name.replace("result_",'').replace('.csv',''))
        sheet.name = tail
        merged += sheet
    merged.save_as(outfilename)

if not os.path.isdir(f"{directory}/../results/excel"):
    os.makedirs(f"{directory}/../results/excel")
input=glob.glob(f"{directory}/../results/*.csv")
merge_csv_to_a_book(input,f"{directory}/../results/excel/output.xlsx")

#раскомментировать, если надо удалить папку results
#shutil.rmtree(f"{directory}/../results")