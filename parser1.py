"""
    Cisco parser
    ~~~~~~~~~~~~~~~~~~~
To use it directly from this file you must install
pip install tkinter
pip install textfsm
pip install xlwt
pip install os
pip install re
pip install pyexcel
pip install pyexcel-xlsx
pip install pyexcel-xlsxw
"""


import textfsm
import os
import re
import glob
from tkinter import filedialog
from tkinter import Tk
from pyexcel.book import Book
from pyexcel.core import save_as, get_sheet
from pyexcel_xlsxw import save_data
# uncomment if you want to delete the results folder
#import shutil
## tkinter

# Closing the system window tkinter
root = Tk()
root.withdraw()

## Function

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



## Dialog window
# Select the directory for the tkinter

directory=filedialog.askdirectory(title='Please select logs directory')

## Reading template files
#Каталог из которого будем брать шаблон

tempdir= filedialog.askdirectory(title='Please select templates directory')
patterns=''

# Get a list of parts of the conversion to the variable arPatFnames

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

##csv output
# create a list of files that will be read

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

##Excel saving

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

# uncomment if you want to delete the results folder
#shutil.rmtree(f"{directory}/../results")