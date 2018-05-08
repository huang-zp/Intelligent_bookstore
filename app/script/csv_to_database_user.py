# coding=utf-8
import csv
import os


FILE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/app/resources/' + 'BX-Users.csv'
with open(FILE_PATH, encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    try:
        for row in f_csv:
            print(row)
    except:
        headers = next(f_csv)

    
        for row in f_csv:
            print(row)