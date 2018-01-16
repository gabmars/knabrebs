import requests
from bs4 import BeautifulSoup
from pyunpack import Archive
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import pyarrow as pa
import gzip
import shutil
import datetime
import json
import sys
import os
#%%
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
def erasing_temp():
    for f in os.listdir('temp'):
        os.unlink('temp\\'+f)
    print('Temp data erased')
def logging(message):
    with open('cbr_log.txt', 'a') as w:
        w.write('{} ({})\n'.format(message, str(datetime.datetime.now())))
        w.close()
#%%
#try:
with open('limitations.json') as d:
    limitations = json.load(d)
    d.close()  
resp = requests.get('http://www.cbr.ru/egrulinfo/?Prtid=egrul1')
soup = BeautifulSoup(resp.text,'lxml')
up_to_date=datetime.datetime.strptime(soup.find('span',{'class':'up_to'}).text,'%d.%m.%Y')
print('Up to '+str(up_to_date.date()))

if up_to_date <= datetime.datetime.strptime(limitations['up_to'],'%Y-%m-%d'):
    logging('Data for {} has already been uploaded to db'.format(limitations['up_to']))
    erasing_temp()
    sys.exit()
link = soup.select_one('p[class="file RAR"]').contents[0]['href']
print('Link recieved')
with open('temp\\'+link, 'wb') as f:
    f.write(requests.get('http://cbr.ru/egrulinfo/{}'.format(link)).content)
    f.close()  
print('Archive downloaded')
try:
    Archive('temp\\'+link).extractall('temp')
except:
    print('')
print('Data extracted')
#%%
filename = 'temp\\UL_LIQUIDATION.csv'
rows = file_len(filename)
data = pd.DataFrame()
batch_size = 100000
max_date=datetime.datetime.strptime(limitations['max_date'],'%Y-%m-%d')
for i in range(int(np.ceil(rows/batch_size))):
    print('{} of {}'.format(i+1, int(np.ceil(rows/batch_size))))
    d = pd.read_csv(filename, sep='\t', warn_bad_lines=False, error_bad_lines=False, skiprows=1+(i*batch_size), nrows=batch_size, encoding='cp1251', dtype=str, header=None).fillna('')
    d[6]=d[6].apply(lambda x: datetime.datetime.strptime(x,'%d.%m.%Y'))
    data = pd.concat([data, d.loc[d[6]>max_date]],ignore_index=True)
data.columns = pd.read_csv(filename, sep='\t', nrows=0, encoding='cp1251', dtype=str).columns
#stat=pd.read_csv('status_dict.csv',delimiter=';',encoding='cp1251')
#status=dict(zip(stat['STATUS_LIQUIDATION_INNER_ID'],stat['NAME']))
#data['STATUS_LIQUIDATION_INNER_ID']=data['STATUS_LIQUIDATION_INNER_ID'].apply(lambda x: status[int(x)])
#for i in data.index:
#    try:
#        data=data.set_value(i,'STATUS_LIQUIDATION_INNER_ID',status[int(data['STATUS_LIQUIDATION_INNER_ID'][i])])
#    except:
#        pass
#%%
with open('limitations.json','w') as d:
    json.dump({'max_date':str(data['DTSTART'].max().date()),'up_to':str(up_to_date.date())},d)
    d.close()
data['DTSTART']=data['DTSTART'].apply(lambda x: x.strftime('%d.%m.%Y'))
data.to_csv('temp\\ul_liq.csv')
print('Data saved to csv')
table = pa.Table.from_pandas(data)
pq.write_table(table, 'ul_liquidation', compression='BROTLI')
print('Data compressed with brotli')
#    with open('ul_liquidation', 'rb') as f_in, gzip.open('ul_liquidation.gz', 'wb') as f_out:
#        shutil.copyfileobj(f_in, f_out)
#    print('Data archived to gzip')
logging('Data for {} downloaded successfully'.format(str(up_to_date)))
#except Exception as e:
#    print('Error:'+str(e))
#    logging(str(e))
#finally:
erasing_temp()