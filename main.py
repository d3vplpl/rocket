__author__ = 'md'
import requests
import os
import zipfile
import csv
import numpy
from datetime import date

CURRENT_YEAR = str(date.today().year)
path_mst = (os.path.join( os.path.curdir, 'mst'))

def get_data():
    url = 'http://bossa.pl/pub/metastock/mstock/mstall.zip'
    print('Getting http://bossa.pl/pub/metastock/mstock/mstall.zip...')
    req = requests.get(url)
    print('Success!')
    if not (os.path.isdir("file")):  #check if directory exists, if not create it
        os.mkdir("file")
    stock_file = open(os.path.join('file', os.path.basename(url)), 'wb')
    for chunk in req.iter_content(100000):
        stock_file.write(chunk)
    stock_file.close()
    zipf = zipfile.ZipFile(os.path.join('file', os.path.basename(url)))
    zipf.extractall((os.path.join( os.path.curdir, 'mst')))

get_data()

files = [f for f in (os.listdir((os.path.join(os.path.curdir, 'mst')))) if os.path.isfile(os.path.join(path_mst, f))]\

for fi in files:

    f = open(os.path.join(path_mst, fi))
    cs = csv.reader(f)
    cs_list = list(cs)
    date_of_last = (cs_list[len(cs_list)-1][1])
    if(date_of_last[:4] ) != CURRENT_YEAR:
        continue

    header = cs_list.pop(0) #removes header
    float_list = []
    ticker = ''
    for el in cs_list:
        ticker = el.pop(0) #removes ticker
        float_list.append([float(i) for i in el])
    n_array = numpy.array(float_list)

    closes = n_array[:, 4]
    float_list = n_array.tolist()
    #print(closes)
    max_close = max(closes)
    last_close = float_list[len(float_list)-1]
    #print(last_close)
    last_close = last_close[4]
    #print(max_close)

    if last_close == max_close:
        print(ticker)


